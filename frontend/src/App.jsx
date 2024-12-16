import { useState, useEffect } from 'react';
import './App.css';
import { TableContainer, Paper, Button, TextField } from '@mui/material';
import CitationsTable from './CitationsTable';
import CitationDialog from './CitationDialog';

const App = () => {
  const proxy = 'http://127.0.0.1:5000/';
  const [data, setData] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isDialogOpen, setDialogOpen] = useState(false);
  const [currentRow, setCurrentRow] = useState(null);
  const [newEntry, setNewEntry] = useState({ author: '', title: '', journal: '', year: '', tags: [], cite_key: '' });
  const [selectedCitations, setSelectedCitations] = useState([]);

  useEffect(() => {
    fetch(proxy + 'citations')
      .then((res) => res.json())
      .then((data) => setData(data))
      .catch((err) => console.log(err));
  }, []);

  const handleOpenDialog = (row = null) => {
    setCurrentRow(row);
    setNewEntry(row || { author: '', title: '', journal: '', year: '', tags: [], cite_key: '' });
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setNewEntry({ author: '', title: '', journal: '', year: '', tags: [], cite_key: '' });
  };

  const handleSave = () => {
    if (currentRow) {
      setData((prev) => prev.map((row) => (row === currentRow ? newEntry : row)));
    } else {
      setData((prev) => [...prev, newEntry]);
    }
    handleCloseDialog();
  };

  const handleDelete = (row) => {
    setData((prev) => prev.filter((item) => item !== row));
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewEntry((prev) => ({ ...prev, [name]: value }));
  };

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleSelectCitation = (cite_key) => {
    setSelectedCitations((prev) =>
      prev.includes(cite_key) ? prev.filter((key) => key !== cite_key) : [...prev, cite_key]
    );
  };

  const filteredData = data.filter((row) => {
    return (
      row.author.toLowerCase().includes(searchQuery.toLowerCase()) ||
      row.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      row.journal.toLowerCase().includes(searchQuery.toLowerCase()) ||
      row.year.toString().includes(searchQuery) ||
      row.tags.join(', ').toLowerCase().includes(searchQuery.toLowerCase()) ||
      row.cite_key.toLowerCase().includes(searchQuery.toLowerCase())
    );
  });

  return (
    <div id="root">
      <h1>Interactive Table</h1>
      <TextField
        label="Search"
        value={searchQuery}
        onChange={handleSearchChange}
        fullWidth
        margin="normal"
        className="search-bar"
      />
      <Button variant="contained" color="primary" onClick={() => handleOpenDialog()}>
        Add New Entry
      </Button>
      <TableContainer component={Paper} className="table-container">
        <CitationsTable
          data={filteredData}
          onEdit={handleOpenDialog}
          onDelete={handleDelete}
          selectedCitations={selectedCitations}
          onSelect={handleSelectCitation}
        />
      </TableContainer>
      <CitationDialog
        isOpen={isDialogOpen}
        onClose={handleCloseDialog}
        onSave={handleSave}
        entry={newEntry}
        onChange={handleInputChange}
        currentRow={currentRow}
      />
    </div>
  );
};

export default App;
