import React from 'react';
import { Dialog, DialogActions, DialogContent, DialogTitle, TextField, Button } from '@mui/material';

const DoiDialog = ({ isOpen, onClose, onSave, doi, onChange }) => {
  return (
    <Dialog open={isOpen} onClose={onClose}>
      <DialogTitle>Add Entry via DOI</DialogTitle>
      <DialogContent>
        <TextField
          label="DOI"
          value={doi}
          onChange={onChange}
          fullWidth
          margin="normal"
        />
      </DialogContent>
      <DialogActions>
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

export default DoiDialog;
