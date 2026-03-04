import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";

const Lienreservationprestation: React.FC = () => {
  return (
    <div id="page-lienreservationprestation-9">
    <div id="icr8w9" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="iq2t7d" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="i67tzg" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="ic1dgu" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="i33qe4" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/centrecongres">{"CentreCongres"}</a>
          <a id="i72t25" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/elementcentre">{"ElementCentre"}</a>
          <a id="iw9l6c" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/indisponibilite">{"Indisponibilite"}</a>
          <a id="iyksxe" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/tarifsaisonnier">{"TarifSaisonnier"}</a>
          <a id="i9gjdd" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reservation">{"Reservation"}</a>
          <a id="i19wkf" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/materiel">{"Materiel"}</a>
          <a id="inw27j" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestation">{"Prestation"}</a>
          <a id="i2yljf" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/lienreservationelement">{"LienReservationElement"}</a>
          <a id="i4uza9" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/lienreservationmateriel">{"LienReservationMateriel"}</a>
          <a id="iwgjkz" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/lienreservationprestation">{"LienReservationPrestation"}</a>
        </div>
        <p id="i0fb6r" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="inxu5r" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="irmamc" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"LienReservationPrestation"}</h1>
        <p id="i73zem" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage LienReservationPrestation data"}</p>
        <TableBlock id="table-lienreservationprestation-9" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="LienReservationPrestation List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Id", "column_type": "field", "field": "id", "type": "str", "required": true}, {"label": "Quantite", "column_type": "field", "field": "quantite", "type": "int", "required": true}, {"label": "CoutCalcule", "column_type": "field", "field": "coutCalcule", "type": "float", "required": true}, {"label": "Inclut", "column_type": "lookup", "path": "inclut", "entity": "Reservation", "field": "id", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "id", "label": "id", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "quantite", "label": "quantite", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "coutCalcule", "label": "coutCalcule", "type": "float", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "prestation", "field": "prestation", "lookup_field": "description", "entity": "Prestation", "type": "str", "required": true}, {"column_type": "lookup", "path": "inclut", "field": "inclut", "lookup_field": "nomContact", "entity": "Reservation", "type": "str", "required": true}]}} dataBinding={{"entity": "LienReservationPrestation", "endpoint": "/lienreservationprestation/"}} />
        <div id="ilutkn" style={{"marginTop": "20px", "display": "flex", "gap": "10px", "flexWrap": "wrap", "--chart-color-palette": "default"}}>
          <MethodButton id="iqmo2v" className="action-button-component" style={{"display": "inline-flex", "alignItems": "center", "padding": "6px 14px", "background": "linear-gradient(90deg, #2563eb 0%, #1e40af 100%)", "color": "#fff", "textDecoration": "none", "borderRadius": "4px", "fontSize": "13px", "fontWeight": "600", "letterSpacing": "0.01em", "cursor": "pointer", "border": "none", "boxShadow": "0 1px 4px rgba(37,99,235,0.10)", "transition": "background 0.2s", "--chart-color-palette": "default"}} endpoint="/lienreservationprestation/{lienreservationprestation_id}/methods/calculerCoutLien/" label="calculerCoutLien" isInstanceMethod={true} instanceSourceTableId="table-lienreservationprestation-9" />
        </div>
      </main>
    </div>    </div>
  );
};

export default Lienreservationprestation;
