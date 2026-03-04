import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";

const Lienreservationmateriel: React.FC = () => {
  return (
    <div id="page-lienreservationmateriel-8">
    <div id="inaiwd" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="ibhs1m" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="iyq15b" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="is3owm" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="i7r7uc" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/centrecongres">{"CentreCongres"}</a>
          <a id="imalty" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/elementcentre">{"ElementCentre"}</a>
          <a id="ik5bbq" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/indisponibilite">{"Indisponibilite"}</a>
          <a id="izrkn1" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/tarifsaisonnier">{"TarifSaisonnier"}</a>
          <a id="izxddr" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reservation">{"Reservation"}</a>
          <a id="i38rht" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/materiel">{"Materiel"}</a>
          <a id="ie3kxd" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestation">{"Prestation"}</a>
          <a id="iy0u0v" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/lienreservationelement">{"LienReservationElement"}</a>
          <a id="iytx0l" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/lienreservationmateriel">{"LienReservationMateriel"}</a>
          <a id="iwmc71" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/lienreservationprestation">{"LienReservationPrestation"}</a>
        </div>
        <p id="i2k8vh" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="itp8z5" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="icc7og" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"LienReservationMateriel"}</h1>
        <p id="ij8hby" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage LienReservationMateriel data"}</p>
        <TableBlock id="table-lienreservationmateriel-8" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="LienReservationMateriel List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Id", "column_type": "field", "field": "id", "type": "str", "required": true}, {"label": "Quantite", "column_type": "field", "field": "quantite", "type": "int", "required": true}, {"label": "CoutCalcule", "column_type": "field", "field": "coutCalcule", "type": "float", "required": true}, {"label": "Inclut", "column_type": "lookup", "path": "inclut", "entity": "Reservation", "field": "id", "type": "list", "required": false}], "formColumns": [{"column_type": "field", "field": "id", "label": "id", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "quantite", "label": "quantite", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "coutCalcule", "label": "coutCalcule", "type": "float", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "inclut", "field": "inclut", "lookup_field": "nomContact", "entity": "Reservation", "type": "list", "required": false}, {"column_type": "lookup", "path": "materiel", "field": "materiel", "lookup_field": "id", "entity": "Materiel", "type": "str", "required": true}]}} dataBinding={{"entity": "LienReservationMateriel", "endpoint": "/lienreservationmateriel/"}} />
        <div id="iuuf2r" style={{"marginTop": "20px", "display": "flex", "gap": "10px", "flexWrap": "wrap", "--chart-color-palette": "default"}}>
          <MethodButton id="ide89r" className="action-button-component" style={{"display": "inline-flex", "alignItems": "center", "padding": "6px 14px", "background": "linear-gradient(90deg, #2563eb 0%, #1e40af 100%)", "color": "#fff", "textDecoration": "none", "borderRadius": "4px", "fontSize": "13px", "fontWeight": "600", "letterSpacing": "0.01em", "cursor": "pointer", "border": "none", "boxShadow": "0 1px 4px rgba(37,99,235,0.10)", "transition": "background 0.2s", "--chart-color-palette": "default"}} endpoint="/lienreservationmateriel/{lienreservationmateriel_id}/methods/calculerCoutLien/" label="calculerCoutLien" parameters={[{"name": "duree", "type": "any", "required": true}]} isInstanceMethod={true} instanceSourceTableId="table-lienreservationmateriel-8" />
        </div>
      </main>
    </div>    </div>
  );
};

export default Lienreservationmateriel;
