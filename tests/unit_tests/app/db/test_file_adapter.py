import unittest

import mock

from src.app.db import file_adapter


class TestFileAdapter(unittest.TestCase):

    @mock.patch('src.app.db.file_adapter.json.dump')
    @mock.patch('src.app.db.file_adapter.FileAdapter.get_all')
    @mock.patch('src.app.db.file_adapter.open', create=True)
    def test__file_adapter__FileAdapter__put__WillAddDocument__WhenTheDocumentIsNotPresentInTheFile(self,
                                                                                                    mock_open,
                                                                                                    mock_get,
                                                                                                    mock_json_dump):

        mock_get.return_value = {}
        mock_outfile = mock_open.return_value.__enter__.return_value

        adapter = file_adapter.FileAdapter('file_name')
        adapter.put({'document_hash': {'id': 'document_hash', 'date': '1234'}})

        mock_json_dump.assert_called_with({'document_hash': {'id': 'document_hash', 'date': '1234'}}, mock_outfile)

    @mock.patch('src.app.db.file_adapter.json.dump')
    @mock.patch('src.app.db.file_adapter.FileAdapter.get_all')
    @mock.patch('src.app.db.file_adapter.open', create=True)
    def test__file_adapter__FileAdapter__put__WillNotDuplicateDocument__WhenTheDocumentIsPresentInTheFile(self,
                                                                                                          mock_open,
                                                                                                          mock_get,
                                                                                                          mock_json_dump):

        mock_get.return_value = {'document_hash': {'id': 'document_hash', 'date': '1234'}}
        mock_outfile = mock_open.return_value.__enter__.return_value
        document_pair = {
            'document_hash': {'id': 'document_hash', 'date': '1234'},
            'second_document': {'id': 'second_document', 'date': '5678'}
        }

        adapter = file_adapter.FileAdapter('file_name')
        adapter.put(document_pair)

        mock_json_dump.assert_called_with(document_pair, mock_outfile)

    @mock.patch('src.app.db.file_adapter.json.dump')
    @mock.patch('src.app.db.file_adapter.FileAdapter.get_all')
    @mock.patch('src.app.db.file_adapter.open', create=True)
    def test__file_adapter__FileAdapter__put__WillAppendNewListToExistingList__WhenADocumentKeyHasAValueOfTypeListAndAlreadyExistsInTheFile(self,
                                                                                                                                            mock_open,
                                                                                                                                            mock_get,
                                                                                                                                            mock_json_dump):
        existing_file_data = {'document_hash': {'id': 'document_hash', 'releases': ['12345']}}
        mock_get.return_value = existing_file_data
        mock_outfile = mock_open.return_value.__enter__.return_value

        adapter = file_adapter.FileAdapter('file_name')
        adapter.put({'document_hash': {'id': 'document_hash', 'releases': ['67890']}})
        merged_dataset = {'document_hash': {'id': 'document_hash', 'releases': ['12345', '67890']}}

        mock_json_dump.assert_called_with(merged_dataset, mock_outfile)

    @mock.patch('src.app.db.file_adapter.json.dump')
    @mock.patch('src.app.db.file_adapter.FileAdapter.get_all')
    @mock.patch('src.app.db.file_adapter.open', create=True)
    def test__file_adapter__FileAdapter__put__WillNotDuplicateListEntries__WhenADocumentKeyHasAListWhichIncludesAValuePresentInTheFile(self,
                                                                                                                                       mock_open,
                                                                                                                                       mock_get,
                                                                                                                                       mock_json_dump):

        existing_file_data = {'document_hash': {'id': 'document_hash', 'releases': ['12345']}}
        mock_get.return_value = existing_file_data
        mock_outfile = mock_open.return_value.__enter__.return_value

        adapter = file_adapter.FileAdapter('file_name')
        adapter.put({'document_hash': {'id': 'document_hash', 'releases': ['12345']}})

        mock_json_dump.assert_called_with(
            {'document_hash': {'id': 'document_hash', 'releases': ['12345']}}, mock_outfile)

    @mock.patch('src.app.db.file_adapter.json.dump')
    @mock.patch('src.app.db.file_adapter.FileAdapter.get_all')
    @mock.patch('src.app.db.file_adapter.open', create=True)
    def test__file_adapter__FileAdapter__put__WillNotReplaceValue__WhenADocumentKeyHasAStringValue(self,
                                                                                                   mock_open,
                                                                                                   mock_get,
                                                                                                   mock_json_dump):

        existing_file_data = {'document_hash': {'id': 'document_hash', 'date': '1234'}}
        mock_get.return_value = existing_file_data
        mock_outfile = mock_open.return_value.__enter__.return_value

        adapter = file_adapter.FileAdapter('file_name')
        adapter.put({'document_hash': {'id': 'document_hash', 'date': '5678'}})

        mock_json_dump.assert_called_with({'document_hash': {'id': 'document_hash', 'date': '1234'}}, mock_outfile)

    @mock.patch('src.app.db.file_adapter.json.dump')
    @mock.patch('src.app.db.file_adapter.FileAdapter.get_all')
    @mock.patch('src.app.db.file_adapter.open', create=True)
    def test__file_adapter__FileAdapter__put__WillNotReplaceValue__WhenADocumentKeyHasAStringValue(self,
                                                                                                   mock_open,
                                                                                                   mock_get,
                                                                                                   mock_json_dump):

        existing_file_data = {'document_hash': {'id': 'document_hash', 'date': '1234'}}
        mock_get.return_value = existing_file_data
        mock_outfile = mock_open.return_value.__enter__.return_value

        adapter = file_adapter.FileAdapter('file_name')
        adapter.put({'document_hash': {'id': 'document_hash', 'date': '5678'}})

        mock_json_dump.assert_called_with(
            {'document_hash': {'id': 'document_hash', 'date': '1234'}}, mock_outfile)

    @mock.patch('src.app.db.file_adapter.json.dump')
    @mock.patch('src.app.db.file_adapter.FileAdapter.get_all')
    @mock.patch('src.app.db.file_adapter.open', create=True)
    def \
            test__file_adapter__FileAdapter__put__WillReplaceValue__WhenADocumentKeyHasAnIntegerValue(self,
                                                                                                  mock_open,
                                                                                                  mock_get,
                                                                                                  mock_json_dump):

        existing_file_data = {'document_hash': {'id': 'document_hash', 'score': 80}}
        mock_get.return_value = existing_file_data
        mock_outfile = mock_open.return_value.__enter__.return_value

        adapter = file_adapter.FileAdapter('file_name')
        adapter.put({'document_hash': {'id': 'document_hash', 'score': 70}})

        mock_json_dump.assert_called_with({'document_hash': {'id': 'document_hash', 'score': 70}}, mock_outfile)