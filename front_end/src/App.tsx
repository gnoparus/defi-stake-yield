import React from 'react';
import { DAppProvider, ChainId } from "@usedapp/core";
import { Header } from "./components/Header"
import { Main } from './components/Main';


function App() {
  return (
    <DAppProvider config={{
      supportedChains: [ChainId.Kovan, ChainId.Rinkeby]
    }}>
      <div>
        <Header />
        Hi!!!
      </div>
      <Main />
    </DAppProvider>

  );
}

export default App;
