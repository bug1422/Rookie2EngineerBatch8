import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy import MetaData
from sqlalchemy.orm import Session

@pytest.fixture
def mock_db_query(multiple_users, multiple_assets):
    """Mock database query object"""
    mock = Mock()
    mock.filter.return_value = mock
    mock.join.return_value = mock
    mock.order_by.return_value = mock
    mock.offset.return_value = mock
    mock.limit.return_value = mock
    
    def get_data(model_type):
        if 'Asset' in str(model_type):
            return multiple_assets
        return multiple_users
    
    mock.count.side_effect = lambda: len(get_data(mock._model))
    mock.all.side_effect = lambda: get_data(mock._model)
    mock.first.side_effect = lambda: get_data(mock._model)[0] if get_data(mock._model) else None
    
    # Store the model type when query() is called
    def query_side_effect(model_type):
        mock._model = model_type
        return mock
    
    mock.query = Mock(side_effect=query_side_effect)
    return mock

@pytest.fixture
def db_session(mock_db_query):
    """Mock database session for testing"""
    session = Mock(spec=Session)
    session.query = mock_db_query.query
    session.add.return_value = None
    session.commit.return_value = None
    session.refresh.return_value = None
    session.delete.return_value = None
    session.close.return_value = None
    return session

@pytest.fixture
def load_metadata(db_session):
    """Fixture to load metadata for tests"""
    metadata = MetaData()
    if isinstance(db_session, Mock):
        mock_bind = MagicMock()
        mock_inspector = MagicMock()
        mock_inspector.get_table_names.return_value = []
        mock_inspector.get_columns.return_value = []
        mock_inspector.get_pk_constraint.return_value = {'constrained_columns': []}
        mock_inspector.get_foreign_keys.return_value = []
        mock_inspector.get_unique_constraints.return_value = []
        mock_inspector.get_check_constraints.return_value = []
        mock_inspector.get_indexes.return_value = []
        
        mock_bind._inspection_context.return_value.__enter__.return_value = mock_inspector
        db_session.bind = mock_bind
        metadata.bind = mock_bind
    else:
        metadata.reflect(bind=db_session.bind)
    return metadata 