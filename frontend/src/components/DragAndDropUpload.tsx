// src/components/DragAndDropUpload/DragAndDropUpload.tsx
import React from "react";
import { useDropzone } from "react-dropzone";
import { Box, Typography } from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import { styled } from "@mui/material/styles";

const StyledBox = styled(Box)(({ theme }) => ({
  width: "50%",
  height: "50%",
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  justifyContent: "center",
  border: `2px dashed ${theme.palette.primary.main}`,
  backgroundColor: theme.palette.background.paper,
  color: theme.palette.text.primary,
  cursor: "pointer",
  "&:hover": {
    backgroundColor: theme.palette.action.hover,
  },
}));

const StyledTypography = styled(Typography)(({ theme }) => ({
  color: theme.palette.text.secondary,
  fontSize: 14,
  textAlign: "center",
}));

const DragAndDropUpload: React.FC = () => {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: (acceptedFiles) => {
      // Handle the files
      console.log(acceptedFiles);
    },
  });

  return (
    <StyledBox {...getRootProps()}>
      <input {...getInputProps()} />
      <CloudUploadIcon sx={{ fontSize: 40, color: "primary.main" }} />
      <StyledTypography>
        {isDragActive
          ? "Drop your jigpuzzle here..."
          : "Drag and drop your jigpuzzle here, or click to select the file"}
      </StyledTypography>
    </StyledBox>
  );
};

export default DragAndDropUpload;
