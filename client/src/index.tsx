import React, { createContext } from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import Store from './store/store';

interface State {
    store: Store,
}

const store = new Store();
export const Context = createContext<State>( {
    store,
})

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <Context.Provider value={{
        store
    }}>
        <BrowserRouter>
            <App />
        </BrowserRouter>
    </Context.Provider>
  </React.StrictMode>
);

