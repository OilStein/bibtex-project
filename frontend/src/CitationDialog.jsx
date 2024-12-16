import React from 'react';
import { Dialog, DialogActions, DialogContent, DialogTitle, TextField, Button } from '@mui/material';
import './App.css';

const CitationDialog = ({ isOpen, onClose, onSave, entry, onChange, currentRow }) => {
  return (
    <Dialog open={isOpen} onClose={onClose}>
      <DialogTitle>{currentRow ? 'Edit Entry' : 'Add New Entry'}</DialogTitle>
      <DialogContent className="dialog-content">
        <TextField
          label="Author"
          name="author"
          value={entry.author}
          onChange={onChange}
          fullWidth
          margin="normal"
        />
        <TextField
          label="Title"
          name="title"
          value={entry.title}
          onChange={onChange}
          fullWidth
          margin="normal"
        />
        <TextField
          label="Journal"
          name="journal"
          value={entry.journal}
          onChange={onChange}
          fullWidth
          margin="normal"
        />
        <TextField
          label="Year"
          name="year"
          value={entry.year}
          onChange={onChange}
          fullWidth
          margin="normal"
        />
        <TextField
          label="Tags (comma separated)"
          name="tags"
          value={entry.tags.join(', ')}
          onChange={onChange}
          fullWidth
          margin="normal"
        />
      </DialogContent>
      <DialogActions className="dialog-actions">
        <Button onClick={onClose} color="secondary">
          Cancel
        </Button>
        <Button onClick={onSave} color="primary">
          Save
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default CitationDialog;
