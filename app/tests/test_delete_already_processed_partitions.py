"""
Unit tests for the delete_already_processed_partitions feature.

This module contains comprehensive pytest-based unit tests for all layers
of the delete_already_processed_partitions feature, following Clean Architecture
principles and best practices.
"""

from unittest.mock import Mock, patch, call
from typing import Any

import pytest

from app.src.features.delete_already_processed_partitions.domain.entities.partition_config import (
    PartitionConfig
)
from app.src.features.delete_already_processed_partitions.domain.entities.table import (
    Table
)
from app.src.features.delete_already_processed_partitions.infra.adapters.awsrangler_data_catalog_adapter import (
    AWSRanglerDataCatalogAdapter
)
from app.src.features.delete_already_processed_partitions.use_case.delete_already_processed_partitions_use_case import (
    DeleteAlreadyProcessedPartitionsUseCase
)
from app.src.features.delete_already_processed_partitions.presentation.delete_already_processed_partitions_presentation import (
    handler
)
from app.src.features.cross.domain.dtos.output_dto import OutputDTO


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sample_partition_config() -> PartitionConfig:
    """Fixture providing a sample partition configuration."""
    return PartitionConfig(
        partition_column="execution_date",
        partition_value="2025-10-28"
    )


@pytest.fixture
def sample_table() -> Table:
    """Fixture providing a sample table entity."""
    return Table(
        database_name="db_test",
        table_name="tbl_test",
        partitions_config=[
            PartitionConfig(
                partition_column="execution_date",
                partition_value="2025-10-28"
            )
        ]
    )


@pytest.fixture
def sample_table_with_multiple_partitions() -> Table:
    """Fixture providing a sample table with multiple partitions."""
    return Table(
        database_name="db_test",
        table_name="tbl_test",
        partitions_config=[
            PartitionConfig(
                partition_column="execution_date",
                partition_value="2025-10-28"
            ),
            PartitionConfig(
                partition_column="execution_date",
                partition_value="2025-10-27"
            )
        ]
    )


@pytest.fixture
def mock_partitions_data() -> dict[str, Any]:
    """Fixture providing mock partition data from AWS Glue."""
    return {
        "s3://bucket/path/execution_date=2025-10-28/": ["2025-10-28"],
        "s3://bucket/path/execution_date=2025-10-27/": ["2025-10-27"],
        "s3://bucket/path/execution_date=2025-10-26/": ["2025-10-26"]
    }


@pytest.fixture
def mock_data_catalog_adapter() -> Mock:
    """Fixture providing a mocked data catalog adapter."""
    adapter = Mock(spec=AWSRanglerDataCatalogAdapter)
    adapter.get_partitions.return_value = {
        "s3://bucket/path/execution_date=2025-10-28/": ["2025-10-28"]
    }
    adapter.check_partition_exists.return_value = True
    adapter.delete_logical_partition_from_data_catalog.return_value = None
    adapter.delete_physical_partition_from_storage.return_value = None
    adapter.delete_processed_partitions.return_value = None
    return adapter


# ============================================================================
# DOMAIN ENTITY TESTS - PartitionConfig
# ============================================================================

def test_should_create_partition_config_with_valid_attributes(sample_partition_config):
    """
    Test that PartitionConfig can be instantiated with valid attributes.
    """
    # Assert
    assert sample_partition_config.partition_column == "execution_date"
    assert sample_partition_config.partition_value == "2025-10-28"


def test_should_create_partition_config_as_dataclass():
    """
    Test that PartitionConfig behaves as a proper dataclass.
    """
    # Arrange & Act
    partition1 = PartitionConfig(
        partition_column="execution_date",
        partition_value="2025-10-28"
    )
    partition2 = PartitionConfig(
        partition_column="execution_date",
        partition_value="2025-10-28"
    )

    # Assert
    assert partition1 == partition2


# ============================================================================
# DOMAIN ENTITY TESTS - Table
# ============================================================================

def test_should_create_table_with_valid_attributes(sample_table):
    """
    Test that Table can be instantiated with valid attributes.
    """
    # Assert
    assert sample_table.database_name == "db_test"
    assert sample_table.table_name == "tbl_test"
    assert len(sample_table.partitions_config) == 1
    assert isinstance(sample_table.partitions_config[0], PartitionConfig)


def test_should_normalize_database_and_table_names_to_lowercase():
    """
    Test that Table normalizes database and table names to lowercase.
    """
    # Arrange & Act
    table = Table(
        database_name="  DB_TEST  ",
        table_name="  TBL_TEST  ",
        partitions_config=[]
    )

    # Assert
    assert table.database_name == "db_test"
    assert table.table_name == "tbl_test"


def test_should_create_table_with_default_partition_config():
    """
    Test that Table creates a default partition configuration when none is provided.
    """
    # Arrange & Act
    table = Table(
        database_name="db_test",
        table_name="tbl_test"
    )

    # Assert
    assert len(table.partitions_config) == 1
    assert table.partitions_config[0].partition_column == "execution_date"
    assert table.partitions_config[0].partition_value is not None


def test_should_create_table_with_multiple_partitions(sample_table_with_multiple_partitions):
    """
    Test that Table can handle multiple partition configurations.
    """
    # Assert
    assert len(sample_table_with_multiple_partitions.partitions_config) == 2
    assert sample_table_with_multiple_partitions.partitions_config[0].partition_value == "2025-10-28"
    assert sample_table_with_multiple_partitions.partitions_config[1].partition_value == "2025-10-27"


# ============================================================================
# INFRASTRUCTURE ADAPTER TESTS - AWSRanglerDataCatalogAdapter
# ============================================================================

@patch("app.src.features.delete_already_processed_partitions.infra.adapters.awsrangler_data_catalog_adapter.wr")
def test_should_get_partitions_successfully(mock_wr, mock_partitions_data):
    """
    Test successful retrieval of partitions from the data catalog.
    """
    # Arrange
    mock_wr.catalog.get_partitions.return_value = mock_partitions_data
    adapter = AWSRanglerDataCatalogAdapter()

    # Act
    result = adapter.get_partitions(
        database_name="db_test",
        table_name="tbl_test"
    )

    # Assert
    assert result == mock_partitions_data
    mock_wr.catalog.get_partitions.assert_called_once_with(
        database="db_test",
        table="tbl_test"
    )


@patch("app.src.features.delete_already_processed_partitions.infra.adapters.awsrangler_data_catalog_adapter.wr")
def test_should_raise_exception_when_get_partitions_fails(mock_wr):
    """
    Test that get_partitions raises an exception when AWS Wrangler fails.
    """
    # Arrange
    mock_wr.catalog.get_partitions.side_effect = Exception("AWS Error")
    adapter = AWSRanglerDataCatalogAdapter()

    # Act & Assert
    with pytest.raises(Exception, match="AWS Error"):
        adapter.get_partitions(
            database_name="db_test",
            table_name="tbl_test"
        )


def test_should_check_partition_exists_returns_true_when_partition_found():
    """
    Test that check_partition_exists returns True when the partition is found.
    """
    # Arrange
    adapter = AWSRanglerDataCatalogAdapter()
    existing_partitions = ["2025-10-28", "2025-10-27", "2025-10-26"]

    # Act
    result = adapter.check_partition_exists(
        existing_partitions_values=existing_partitions,
        partition_value_to_delete="2025-10-28"
    )

    # Assert
    assert result is True


def test_should_check_partition_exists_returns_false_when_partition_not_found():
    """
    Test that check_partition_exists returns False when the partition is not found.
    """
    # Arrange
    adapter = AWSRanglerDataCatalogAdapter()
    existing_partitions = ["2025-10-28", "2025-10-27", "2025-10-26"]

    # Act
    result = adapter.check_partition_exists(
        existing_partitions_values=existing_partitions,
        partition_value_to_delete="2025-10-25"
    )

    # Assert
    assert result is False


@patch("app.src.features.delete_already_processed_partitions.infra.adapters.awsrangler_data_catalog_adapter.wr")
def test_should_delete_logical_partition_from_data_catalog_successfully(mock_wr):
    """
    Test successful deletion of logical partition from the data catalog.
    """
    # Arrange
    adapter = AWSRanglerDataCatalogAdapter()

    # Act
    adapter.delete_logical_partition_from_data_catalog(
        database_name="db_test",
        table_name="tbl_test",
        partition_values=[["2025-10-28"]]
    )

    # Assert
    mock_wr.catalog.delete_partitions.assert_called_once_with(
        database="db_test",
        table="tbl_test",
        partitions_values=[["2025-10-28"]]
    )


@patch("app.src.features.delete_already_processed_partitions.infra.adapters.awsrangler_data_catalog_adapter.wr")
def test_should_raise_exception_when_delete_logical_partition_fails(mock_wr):
    """
    Test that delete_logical_partition raises an exception when deletion fails.
    """
    # Arrange
    mock_wr.catalog.delete_partitions.side_effect = Exception("Delete Error")
    adapter = AWSRanglerDataCatalogAdapter()

    # Act & Assert
    with pytest.raises(Exception, match="Delete Error"):
        adapter.delete_logical_partition_from_data_catalog(
            database_name="db_test",
            table_name="tbl_test",
            partition_values=[["2025-10-28"]]
        )


@patch("app.src.features.delete_already_processed_partitions.infra.adapters.awsrangler_data_catalog_adapter.wr")
def test_should_delete_physical_partition_from_storage_successfully(mock_wr):
    """
    Test successful deletion of physical partition from S3 storage.
    """
    # Arrange
    adapter = AWSRanglerDataCatalogAdapter()
    partition_path = "s3://bucket/path/execution_date=2025-10-28/"

    # Act
    adapter.delete_physical_partition_from_storage(partition_path=partition_path)

    # Assert
    mock_wr.s3.delete_objects.assert_called_once_with(path=partition_path)


@patch("app.src.features.delete_already_processed_partitions.infra.adapters.awsrangler_data_catalog_adapter.wr")
def test_should_raise_exception_when_delete_physical_partition_fails(mock_wr):
    """
    Test that delete_physical_partition raises an exception when deletion fails.
    """
    # Arrange
    mock_wr.s3.delete_objects.side_effect = Exception("S3 Error")
    adapter = AWSRanglerDataCatalogAdapter()

    # Act & Assert
    with pytest.raises(Exception, match="S3 Error"):
        adapter.delete_physical_partition_from_storage(
            partition_path="s3://bucket/path/execution_date=2025-10-28/"
        )


@patch("app.src.features.delete_already_processed_partitions.infra.adapters.awsrangler_data_catalog_adapter.wr")
def test_should_delete_processed_partitions_for_single_table(mock_wr, sample_table):
    """
    Test deletion of processed partitions for a single table.
    """
    # Arrange
    mock_wr.catalog.get_partitions.return_value = {
        "s3://bucket/path/execution_date=2025-10-28/": ["2025-10-28"]
    }
    adapter = AWSRanglerDataCatalogAdapter()

    # Act
    adapter.delete_processed_partitions(tables=[sample_table])

    # Assert
    mock_wr.catalog.get_partitions.assert_called_once_with(
        database="db_test",
        table="tbl_test"
    )
    mock_wr.catalog.delete_partitions.assert_called_once()
    mock_wr.s3.delete_objects.assert_called_once()


@patch("app.src.features.delete_already_processed_partitions.infra.adapters.awsrangler_data_catalog_adapter.wr")
def test_should_not_delete_partition_when_partition_does_not_exist(mock_wr, sample_table):
    """
    Test that no deletion occurs when the partition does not exist.
    """
    # Arrange
    mock_wr.catalog.get_partitions.return_value = {
        "s3://bucket/path/execution_date=2025-10-27/": ["2025-10-27"]
    }
    adapter = AWSRanglerDataCatalogAdapter()

    # Act
    adapter.delete_processed_partitions(tables=[sample_table])

    # Assert
    mock_wr.catalog.get_partitions.assert_called_once()
    mock_wr.catalog.delete_partitions.assert_not_called()
    mock_wr.s3.delete_objects.assert_not_called()


@patch("app.src.features.delete_already_processed_partitions.infra.adapters.awsrangler_data_catalog_adapter.wr")
def test_should_delete_processed_partitions_for_multiple_tables(mock_wr):
    """
    Test deletion of processed partitions for multiple tables.
    """
    # Arrange
    mock_wr.catalog.get_partitions.return_value = {
        "s3://bucket/path/execution_date=2025-10-28/": ["2025-10-28"]
    }
    adapter = AWSRanglerDataCatalogAdapter()
    tables = [
        Table(
            database_name="db_test1",
            table_name="tbl_test1",
            partitions_config=[
                PartitionConfig(
                    partition_column="execution_date",
                    partition_value="2025-10-28"
                )
            ]
        ),
        Table(
            database_name="db_test2",
            table_name="tbl_test2",
            partitions_config=[
                PartitionConfig(
                    partition_column="execution_date",
                    partition_value="2025-10-28"
                )
            ]
        )
    ]

    # Act
    adapter.delete_processed_partitions(tables=tables)

    # Assert
    assert mock_wr.catalog.get_partitions.call_count == 2
    assert mock_wr.catalog.delete_partitions.call_count == 2
    assert mock_wr.s3.delete_objects.call_count == 2


@patch("app.src.features.delete_already_processed_partitions.infra.adapters.awsrangler_data_catalog_adapter.wr")
def test_should_delete_multiple_partitions_for_same_table(mock_wr, sample_table_with_multiple_partitions):
    """
    Test deletion of multiple partitions for the same table.
    """
    # Arrange
    mock_wr.catalog.get_partitions.return_value = {
        "s3://bucket/path/execution_date=2025-10-28/": ["2025-10-28"],
        "s3://bucket/path/execution_date=2025-10-27/": ["2025-10-27"]
    }
    adapter = AWSRanglerDataCatalogAdapter()

    # Act
    adapter.delete_processed_partitions(tables=[sample_table_with_multiple_partitions])

    # Assert
    mock_wr.catalog.get_partitions.assert_called_once()
    assert mock_wr.catalog.delete_partitions.call_count == 2
    assert mock_wr.s3.delete_objects.call_count == 2


# ============================================================================
# USE CASE TESTS - DeleteAlreadyProcessedPartitionsUseCase
# ============================================================================

def test_should_execute_use_case_successfully(mock_data_catalog_adapter):
    """
    Test successful execution of the delete already processed partitions use case.
    """
    # Arrange
    use_case = DeleteAlreadyProcessedPartitionsUseCase(
        data_catalog_adapter=mock_data_catalog_adapter
    )

    # Act
    result = use_case.execute()

    # Assert
    assert isinstance(result, OutputDTO)
    assert result.success is True
    assert result.data is not None
    assert "tables_cleaned_up" in result.data
    assert len(result.data["tables_cleaned_up"]) == 3
    mock_data_catalog_adapter.delete_processed_partitions.assert_called_once()


def test_should_execute_use_case_with_correct_tables_configuration(mock_data_catalog_adapter):
    """
    Test that the use case executes with the correct pre-configured tables.
    """
    # Arrange
    use_case = DeleteAlreadyProcessedPartitionsUseCase(
        data_catalog_adapter=mock_data_catalog_adapter
    )

    # Act
    result = use_case.execute()

    # Assert
    tables = result.data["tables_cleaned_up"]
    table_names = [t.table_name for t in tables]
    
    assert "sor_tbl_b3stocks_active_stocks" in table_names
    assert "sor_tbl_b3stocks_fundamentus_eod_stock_metrics" in table_names
    assert "sor_tbl_b3stocks_batch_process_control" in table_names
    
    # Verify all tables belong to the same database
    for table in tables:
        assert table.database_name == "db_b3stocks_analytics_sor"


def test_should_raise_exception_when_use_case_execution_fails(mock_data_catalog_adapter):
    """
    Test that the use case raises an exception when deletion fails.
    """
    # Arrange
    mock_data_catalog_adapter.delete_processed_partitions.side_effect = Exception("Deletion Error")
    use_case = DeleteAlreadyProcessedPartitionsUseCase(
        data_catalog_adapter=mock_data_catalog_adapter
    )

    # Act & Assert
    with pytest.raises(Exception, match="Deletion Error"):
        use_case.execute()


def test_should_pass_correct_tables_to_adapter(mock_data_catalog_adapter):
    """
    Test that the use case passes the correct tables to the data catalog adapter.
    """
    # Arrange
    use_case = DeleteAlreadyProcessedPartitionsUseCase(
        data_catalog_adapter=mock_data_catalog_adapter
    )

    # Act
    use_case.execute()

    # Assert
    mock_data_catalog_adapter.delete_processed_partitions.assert_called_once()
    call_args = mock_data_catalog_adapter.delete_processed_partitions.call_args
    tables_argument = call_args.kwargs["tables"]
    
    assert len(tables_argument) == 3
    assert all(isinstance(t, Table) for t in tables_argument)


# ============================================================================
# PRESENTATION LAYER TESTS - handler
# ============================================================================

@patch("app.src.features.delete_already_processed_partitions.presentation.delete_already_processed_partitions_presentation.use_case")
@patch("app.src.features.delete_already_processed_partitions.presentation.delete_already_processed_partitions_presentation.HTTPResponseMapper")
def test_should_execute_handler_successfully(mock_mapper, mock_use_case):
    """
    Test successful execution of the Lambda handler function.
    """
    # Arrange
    mock_output = OutputDTO.ok(data={"tables_cleaned_up": []})
    mock_use_case.execute.return_value = mock_output
    mock_mapper.map.return_value = {"statusCode": 200, "body": "{}"}
    
    event = {}
    context = None

    # Act
    result = handler(event, context)

    # Assert
    mock_use_case.execute.assert_called_once()
    mock_mapper.map.assert_called_once_with(mock_output)
    assert result == {"statusCode": 200, "body": "{}"}


@patch("app.src.features.delete_already_processed_partitions.presentation.delete_already_processed_partitions_presentation.use_case")
@patch("app.src.features.delete_already_processed_partitions.presentation.delete_already_processed_partitions_presentation.HTTPResponseMapper")
def test_should_handle_use_case_output_correctly(mock_mapper, mock_use_case):
    """
    Test that the handler correctly processes the use case output.
    """
    # Arrange
    tables_data = [
        Table(database_name="db_test", table_name="tbl_test", partitions_config=[])
    ]
    mock_output = OutputDTO.ok(data={"tables_cleaned_up": tables_data})
    mock_use_case.execute.return_value = mock_output
    mock_mapper.map.return_value = {"statusCode": 200}

    # Act
    handler({}, None)

    # Assert
    mock_mapper.map.assert_called_once()
    call_args = mock_mapper.map.call_args[0][0]
    assert call_args.success is True
    assert call_args.data["tables_cleaned_up"] == tables_data


@patch("app.src.features.delete_already_processed_partitions.presentation.delete_already_processed_partitions_presentation.use_case")
@patch("app.src.features.delete_already_processed_partitions.presentation.delete_already_processed_partitions_presentation.HTTPResponseMapper")
def test_should_handle_use_case_exception_in_handler(mock_mapper, mock_use_case):
    """
    Test that the handler propagates exceptions from the use case.
    """
    # Arrange
    mock_use_case.execute.side_effect = Exception("Use Case Error")

    # Act & Assert
    with pytest.raises(Exception, match="Use Case Error"):
        handler({}, None)


@patch("app.src.features.delete_already_processed_partitions.presentation.delete_already_processed_partitions_presentation.use_case")
@patch("app.src.features.delete_already_processed_partitions.presentation.delete_already_processed_partitions_presentation.HTTPResponseMapper")
def test_should_call_handler_with_empty_event(mock_mapper, mock_use_case):
    """
    Test that the handler can be called with an empty event dictionary.
    """
    # Arrange
    mock_output = OutputDTO.ok(data={})
    mock_use_case.execute.return_value = mock_output
    mock_mapper.map.return_value = {"statusCode": 200}

    # Act
    result = handler({}, None)

    # Assert
    assert result is not None
    mock_use_case.execute.assert_called_once()
