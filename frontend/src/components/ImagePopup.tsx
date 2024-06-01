import React from "react";
import { Dialog, DialogContent, IconButton } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";

interface ImagePopupProps {
  imageUrl: string;
  onClose: () => void;
}

const ImagePopup: React.FC<ImagePopupProps> = ({ imageUrl, onClose }) => {
  return (
    <Dialog open={imageUrl !== ""} onClose={onClose} maxWidth="md" fullWidth>
      <IconButton
        aria-label="close"
        onClick={onClose}
        sx={{
          position: "absolute",
          right: 8,
          top: 8,
          color: (theme) => theme.palette.grey[500],
        }}
      >
        <CloseIcon />
      </IconButton>
      <DialogContent>
        <img
          src={imageUrl}
          alt="Uploaded"
          style={{ width: "100%", height: "auto" }}
        />
      </DialogContent>
    </Dialog>
  );
};

export default ImagePopup;
