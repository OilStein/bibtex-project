import { useState, useEffect } from 'react'
import './App.css'
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  TextField,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
} from '@mui/material';

const App = () => {

  const proxy = 'http://127.0.0.1:5000/'


  const [data, setData] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');

  const [isDialogOpen, setDialogOpen] = useState(false);
  const [currentRow, setCurrentRow] = useState(null);
  const [newEntry, setNewEntry] = useState({ author: '', title: '', journal: '', year: '', tags: [], cite_key: '' });

  useEffect(() => {
    fetch(proxy + 'citations')
      .then((res) => res.json())
      .then((data) => setData(data))
      .catch((err) => console.log(err));
    console.log(data)
  }, []);

  const handleOpenDialog = (row = null) => {
    setCurrentRow(row);
    setNewEntry(row || { author: '', title: '', journal: '', year: '' });
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setNewEntry({ author: '', title: '', journal: '', year: '' });
  };

  const handleSave = () => {
    if (currentRow) {
      // Update existing entry
      setData((prev) =>
        prev.map((row) => (row === currentRow ? newEntry : row))
      );
    } else {
      // Add new entry
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

  const formatTags = (tags) => {
    return tags.join(', ');
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>Interactive Table</h1>
      <TextField
        label="Search"
        value={searchQuery}
        onChange={handleSearchChange}
        fullWidth
        margin="normal"
      />
      <Button variant="contained" color="primary" onClick={() => handleOpenDialog()}>
        Add New Entry
      </Button>
      <TableContainer component={Paper} style={{ marginTop: '20px' }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Key</TableCell>
              <TableCell>Author</TableCell>
              <TableCell>Title</TableCell>
              <TableCell>Journal</TableCell>
              <TableCell>Year</TableCell>
              <TableCell>Tags</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredData.map((row, index) => (
              <TableRow key={index}>
                <TableCell>{row.cite_key}</TableCell>
                <TableCell>{row.author}</TableCell>
                <TableCell>{row.title}</TableCell>
                <TableCell>{row.journal}</TableCell>
                <TableCell>{row.year}</TableCell>
                <TableCell>{formatTags(row.tags)}</TableCell>
                <TableCell>
                  <Button
                    variant="outlined"
                    color="primary"
                    onClick={() => handleOpenDialog(row)}
                    style={{ marginRight: '10px' }}
                  >
                    Edit
                  </Button>
                  <Button variant="outlined" color="secondary" onClick={() => handleDelete(row)}>
                    Delete
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Dialog for Adding/Editing */}
      <Dialog open={isDialogOpen} onClose={handleCloseDialog}>
        <DialogTitle>{currentRow ? 'Edit Entry' : 'Add New Entry'}</DialogTitle>
        <DialogContent>
          <TextField
            label="Author"
            name="author"
            value={newEntry.author}
            onChange={handleInputChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Title"
            name="title"
            value={newEntry.title}
            onChange={handleInputChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Journal"
            name="journal"
            value={newEntry.journal}
            onChange={handleInputChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Year"
            name="year"
            value={newEntry.year}
            onChange={handleInputChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Tags"
            name="tags"
            value={newEntry.tags}
            onChange={handleInputChange}
            fullWidth
            margin="normal"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog} color="secondary">
            Cancel
          </Button>
          <Button onClick={handleSave} color="primary">
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default App
