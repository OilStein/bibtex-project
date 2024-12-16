import React from 'react';
import { Table, TableBody, TableCell, TableHead, TableRow, Button, Checkbox } from '@mui/material';

const CitationsTable = ({ data, onEdit, onDelete, selectedCitations, onSelect }) => {
  const formatTags = (tags) => {
    return tags.join(', ');
  };

  const isSelected = (row) => (selectedCitations || []).includes(row.cite_key);

  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>Select</TableCell>
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
        {data.map((row, index) => (
          <TableRow key={index}>
            <TableCell>
              <Checkbox
                checked={isSelected(row)}
                onChange={() => onSelect(row.cite_key)}
              />
            </TableCell>
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
                onClick={() => onEdit(row)}
                style={{ marginRight: '10px' }}
              >
                Edit
              </Button>
              <Button variant="outlined" color="secondary" onClick={() => onDelete(row)}>
                Delete
              </Button>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

export default CitationsTable;
