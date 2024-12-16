import { useState, useEffect } from 'react';
import './App.css';
import { TableContainer, Paper, Button, TextField } from '@mui/material';
import CitationsTable from './CitationsTable';
import CitationDialog from './CitationDialog';
import DoiDialog from './DoiDialog';

const App = () => {
  const proxy = 'http://127.0.0.1:5000/';
  const [data, setData] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isDialogOpen, setDialogOpen] = useState(false);
  const [isDoiDialogOpen, setDoiDialogOpen] = useState(false);
  const [currentRow, setCurrentRow] = useState(null);
  const [newEntry, setNewEntry] = useState({ author: '', title: '', journal: '', year: 0, tags: [], cite_key: '' });
  const [selectedCitations, setSelectedCitations] = useState([]);
  const [doi, setDoi] = useState('');

  useEffect(() => {
    fetch(proxy + 'citations')
      .then((res) => {
        if (res.status === 200) {
          return res.json();
        } else {
          throw new Error('Failed to fetch citations');
        }
      })
      .then((data) => setData(data))
      .catch((err) => console.log(err));
  }, []);

  const handleOpenDialog = (row = null) => {
    setCurrentRow(row);
    setNewEntry(row || { author: '', title: '', journal: '', year: 0, tags: [], cite_key: '' });
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setNewEntry({ author: '', title: '', journal: '', year: '', tags: [], cite_key: '' });
  };

  const handleOpenDoiDialog = () => {
    setDoiDialogOpen(true);
  };

  const handleCloseDoiDialog = () => {
    setDoiDialogOpen(false);
    setDoi('');
  };

  const handleSave = () => {
    let endpoint = currentRow ? proxy + 'citations/' + currentRow.cite_key : proxy + 'citations';
    fetch(endpoint, {
      method: currentRow ? 'PUT' : 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newEntry),
    })
      .then((res) => {
        if (res.status === 201 || res.status === 200) {
          return res.json();
        } else {
          throw new Error('Failed to save citation');
        }
      })
      .then((data) => {
        if (currentRow) {
          setData((prev) => prev.map((item) => (item.cite_key === data.cite_key ? data : item)));
        } else {
          setData((prev) => [...prev, data]);
        }
        handleCloseDialog();
      })
  };

  const handleSaveDoi = () => {
    fetch(proxy + 'doi', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ doi }),
    })
      .then((res) => {
        if (res.status === 201 || res.status === 200) {
          return res.json();
        } else {
          throw new Error('Failed to save DOI');
        }
      })
      .then((data) => {
        setData((prev) => [...prev, data]);
        setDoi('');
        handleCloseDoiDialog();
      })
      .catch((err) => console.log(err));
  };


  const handleDelete = (row) => {
    fetch(proxy + 'citations' + row.cite_key, {
      method: 'DELETE',
    })
      .then((res) => {
        if (res.status === 204) {
          setData((prev) => prev.filter((item) => item.cite_key !== row.cite_key));
        } else {
          throw new Error('Failed to delete citation');
        }
      })
      .catch((err) => console.log(err));
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (name === 'tags') {
      setNewEntry((prev) => ({ ...prev, tags: value.split(',').map(tag => tag.trim()) }));
    } else if (name === 'year') {
      setNewEntry((prev) => ({ ...prev, [name]: Number(value) }));
    } else {
      setNewEntry((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleDoiChange = (e) => {
    setDoi(e.target.value);
  };

  const handleSelectCitation = (cite_key) => {
    setSelectedCitations((prev) =>
      prev.includes(cite_key) ? prev.filter((key) => key !== cite_key) : [...prev, cite_key]
    );
  };

  const handleDownloadBibtex = () => {
    fetch(proxy + 'bibtex', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ keys: selectedCitations }),
    })
      .then((res) => {
        if (res.status === 200) {
          return res.blob();
        } else {
          throw new Error('Failed to download Bibtex');
        }
      })
      .then((blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'dd.txt';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      })
      .catch((err) => console.log(err));
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
      <h1>Bibtex Project</h1>
      <TextField
        label="Search"
        value={searchQuery}
        onChange={handleSearchChange}
        fullWidth
        margin="normal"
        className="search-bar"
      />
      <div className="add-entry-container">
        <Button variant="contained" color="primary" onClick={() => handleOpenDialog()}>
          Add New Entry
        </Button>
        <Button variant="contained" color="secondary" onClick={handleOpenDoiDialog}>
          Add via DOI
        </Button>
        <Button variant="contained" color="default" onClick={handleDownloadBibtex}>
          Download Bibtex
        </Button>
      </div>
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
      <DoiDialog
        isOpen={isDoiDialogOpen}
        onClose={handleCloseDoiDialog}
        onSave={handleSaveDoi}
        doi={doi}
        onChange={handleDoiChange}
      />
    </div>
  );
};

export default App;
