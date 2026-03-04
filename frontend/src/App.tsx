import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { TableProvider } from "./contexts/TableContext";
import Centrecongres from "./pages/Centrecongres";
import Lienreservationprestation from "./pages/Lienreservationprestation";
import Elementcentre from "./pages/Elementcentre";
import Indisponibilite from "./pages/Indisponibilite";
import Tarifsaisonnier from "./pages/Tarifsaisonnier";
import Reservation from "./pages/Reservation";
import Materiel from "./pages/Materiel";
import Prestation from "./pages/Prestation";
import Lienreservationelement from "./pages/Lienreservationelement";
import Lienreservationmateriel from "./pages/Lienreservationmateriel";

function App() {
  return (
    <TableProvider>
      <div className="app-container">
        <main className="app-main">
          <Routes>
            <Route path="/centrecongres" element={<Centrecongres />} />
            <Route path="/lienreservationprestation" element={<Lienreservationprestation />} />
            <Route path="/elementcentre" element={<Elementcentre />} />
            <Route path="/indisponibilite" element={<Indisponibilite />} />
            <Route path="/tarifsaisonnier" element={<Tarifsaisonnier />} />
            <Route path="/reservation" element={<Reservation />} />
            <Route path="/materiel" element={<Materiel />} />
            <Route path="/prestation" element={<Prestation />} />
            <Route path="/lienreservationelement" element={<Lienreservationelement />} />
            <Route path="/lienreservationmateriel" element={<Lienreservationmateriel />} />
            <Route path="/" element={<Navigate to="/centrecongres" replace />} />
            <Route path="*" element={<Navigate to="/centrecongres" replace />} />
          </Routes>
        </main>
      </div>
    </TableProvider>
  );
}
export default App;
