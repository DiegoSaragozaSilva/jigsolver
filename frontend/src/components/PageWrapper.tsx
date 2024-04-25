// src/components/PageWrapper/PageWrapper.tsx
import React, { ReactNode } from "react";
import { Box } from "@mui/material";
import { styled } from "@mui/material/styles";

interface PageWrapperProps {
  children: ReactNode;
}

const StyledBox = styled(Box)(({ theme }) => ({
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
  alignItems: "center",
  height: "100%",
  width: "100%",
  backgroundColor: theme.palette.background.default,
  color: theme.palette.text.primary,
}));

const PageWrapper: React.FC<PageWrapperProps> = ({ children }) => {
  return (
    <div style={{ height: "100vh" }}>
      <StyledBox>{children}</StyledBox>
    </div>
  );
};

export default PageWrapper;
