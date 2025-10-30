// ConfirmDialog.jsx
import React from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
  Slide
} from "@mui/material";
import { WarningAmber } from "@mui/icons-material";

// Slide animation for dialog
const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="down" ref={ref} {...props} />;
});

export default function ConfirmDialog({
  open,
  title = "Confirm",
  message = "Are you sure?",
  onClose,
  onConfirm,
  confirmText = "Yes",
  cancelText = "Cancel",
}) {
  return (
    <Dialog
      open={open}
      onClose={onClose}
      slots={{ transition: Transition }}
      slotProps={{
        paper: {
          sx: {
            borderRadius: 3,
            boxShadow: 8,
            minWidth: 360,
          },
        },
      }}
      aria-labelledby="confirm-dialog-title"
      aria-describedby="confirm-dialog-description"
    >
      <DialogTitle
        id="confirm-dialog-title"
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 1,
          fontWeight: "bold",
          fontSize: "1.25rem",
        }}
      >
        <WarningAmber color="warning" fontSize="medium" />
        {title}
      </DialogTitle>
      <DialogContent>
        <DialogContentText
          id="confirm-dialog-description"
          sx={{ fontSize: "1rem", color: "text.secondary" }}
        >
          {message}
        </DialogContentText>
      </DialogContent>
      <DialogActions sx={{ px: 3, pb: 2 }}>
        <Button onClick={onClose} variant="outlined" color="inherit">
          {cancelText}
        </Button>
        <Button
          onClick={onConfirm}
          variant="contained"
          color="error"
          sx={{ ml: 1 }}
        >
          {confirmText}
        </Button>
      </DialogActions>
    </Dialog>
  );
}