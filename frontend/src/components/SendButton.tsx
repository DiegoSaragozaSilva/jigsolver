import React from "react";
import { Button } from "@mui/material";
import { styled } from "@mui/material/styles";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import ImageIcon from "@mui/icons-material/Image";

interface SendButtonProps {
  onSend: () => void;
  file: File | null;
}

const StyledButton = styled(Button)(({ theme }) => ({
  background: theme.palette.secondary.main,
  "&:hover": {
    background: theme.palette.secondary.dark,
  },
  margin: theme.spacing(1),
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
}));

const SendButton: React.FC<SendButtonProps> = ({ onSend, file }) => {
  return (
    <StyledButton variant="contained" onClick={onSend}>
      {file && (
        <>
          <ImageIcon style={{ marginRight: 8 }} />
          <span>{file.name}</span>
        </>
      )}
      <ArrowForwardIcon style={{ marginLeft: "auto" }} />
    </StyledButton>
  );
};

export default SendButton;
