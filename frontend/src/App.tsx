import React, { useState } from "react";
import { ThemeProvider } from "@mui/material/styles";

import draculaTheme from "./theme";
import PageWrapper from "./components/PageWrapper";
import Header from "./components/Header";
import DragAndDropUpload from "./components/DragAndDropUpload";

const App: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);

  const handleFileUpload = (file: File) => {
    setFile(file);
    // You can also start the jigsaw solving process here or handle it as needed
  };

  return (
    <div>
      <ThemeProvider theme={draculaTheme}>
        <Header />
        <PageWrapper>
          <DragAndDropUpload />
        </PageWrapper>
      </ThemeProvider>
      ,
    </div>
  );
};

export default App;
