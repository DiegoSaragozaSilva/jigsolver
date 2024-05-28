import React, { ReactNode } from "react";
import { useTheme } from "@mui/material/styles";

interface PageWrapperProps {
  children: ReactNode;
  height?: string;
}

const PageWrapper: React.FC<PageWrapperProps> = ({
  children,
  height = "100vh",
}) => {
  const theme = useTheme();

  return (
    <div
      style={{
        height: height,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        width: "100%",
        backgroundColor: theme.palette.background.default,
        color: theme.palette.text.primary,
      }}
    >
      {children}
    </div>
  );
};

export default PageWrapper;
