import mock
import unittest
from app.db import file_adapter


class TestFileAdapter(unittest.TestCase):

    @mock.patch('app.db.file_adapter.json.dump')
    @mock.patch('app.db.file_adapter.FileAdapter.get')
    @mock.patch('app.db.file_adapter.open', create=True)
    def test__file_adapter__FileAdapter__put__WillAppendNewListToExistingList__WhenADocumentKeyHasAValueOfTypeListAndAlreadyExistsInTheFile(self,
                                                                                                                                            mock_open,
                                                                                                                                            mock_get,
                                                                                                                                            mock_json_dump):
        existing_file_data = {'document_hash': {'id': 'document_hash', 'release': ['12345']}}
        mock_get.return_value = existing_file_data
        mock_outfile = mock_open.return_value.__enter__.return_value

        adapter = file_adapter.FileAdapter('file_name')
        adapter.put({'document_hash': {'id': 'document_hash', 'release': ['67890']}})

        mock_json_dump.assert_called_with({'document_hash': {'id': 'document_hash', 'release': ['12345', '67890']}}, mock_outfile)

    @mock.patch('app.db.file_adapter.json.dump')
    @mock.patch('app.db.file_adapter.FileAdapter.get')
    @mock.patch('app.db.file_adapter.open', create=True)
    def test__file_adapter__FileAdapter__put__WillNotDuplicateListEntries__WhenADocumentKeyHasAListWhichIncludesAValuePresentInTheFile(
            self,
            mock_open,
            mock_get,
            mock_json_dump):

        existing_file_data = {'document_hash': {'id': 'document_hash', 'release': ['12345']}}
        mock_get.return_value = existing_file_data
        mock_outfile = mock_open.return_value.__enter__.return_value

        adapter = file_adapter.FileAdapter('file_name')
        adapter.put({'document_hash': {'id': 'document_hash', 'release': ['12345']}})

        mock_json_dump.assert_called_with(
            {'document_hash': {'id': 'document_hash', 'release': ['12345']}}, mock_outfile)