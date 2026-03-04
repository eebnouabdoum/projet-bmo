import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";

const Materiel: React.FC = () => {
  return (
    <div id="page-materiel-5">
    <div id="ilrpba" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="ixuwmy" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="icx8ee" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="i3r2gg" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="iwxv2i" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/centrecongres">{"CentreCongres"}</a>
          <a id="iwi2ou" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/elementcentre">{"ElementCentre"}</a>
          <a id="ie2qqh" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/indisponibilite">{"Indisponibilite"}</a>
          <a id="ib8mwc" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/tarifsaisonnier">{"TarifSaisonnier"}</a>
          <a id="it0clg" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reservation">{"Reservation"}</a>
          <a id="io328d" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/materiel">{"Materiel"}</a>
          <a id="ipulhf" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestation">{"Prestation"}</a>
          <a id="imh7qx" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/lienreservationelement">{"LienReservationElement"}</a>
          <a id="i1otpc" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/lienreservationmateriel">{"LienReservationMateriel"}</a>
          <a id="i53pwg" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/lienreservationprestation">{"LienReservationPrestation"}</a>
        </div>
        <p id="iioc9i" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="ijrut1" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="iml84k" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Materiel"}</h1>
        <p id="iduatl" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage Materiel data"}</p>
        <TableBlock id="table-materiel-5" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Materiel List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Id", "column_type": "field", "field": "id", "type": "str", "required": true}, {"label": "Nom", "column_type": "field", "field": "nom", "type": "str", "required": true}, {"label": "Description", "column_type": "field", "field": "description", "type": "str", "required": true}, {"label": "PrixJournalierBase", "column_type": "field", "field": "prixJournalierBase", "type": "float", "required": true}, {"label": "StockTotal", "column_type": "field", "field": "stockTotal", "type": "int", "required": true}], "formColumns": [{"column_type": "field", "field": "id", "label": "id", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "nom", "label": "nom", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "description", "label": "description", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "prixJournalierBase", "label": "prixJournalierBase", "type": "float", "required": true, "defaultValue": null}, {"column_type": "field", "field": "stockTotal", "label": "stockTotal", "type": "int", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "lienreservationmateriel_1", "field": "lienreservationmateriel_1", "lookup_field": "id", "entity": "LienReservationMateriel", "type": "list", "required": false}]}} dataBinding={{"entity": "Materiel", "endpoint": "/materiel/"}} />
        <div id="i09ekk" style={{"marginTop": "20px", "display": "flex", "gap": "10px", "flexWrap": "wrap", "--chart-color-palette": "default"}}>
          <MethodButton id="ipcqek" className="action-button-component" style={{"display": "inline-flex", "alignItems": "center", "padding": "6px 14px", "background": "linear-gradient(90deg, #2563eb 0%, #1e40af 100%)", "color": "#fff", "textDecoration": "none", "borderRadius": "4px", "fontSize": "13px", "fontWeight": "600", "letterSpacing": "0.01em", "cursor": "pointer", "border": "none", "boxShadow": "0 1px 4px rgba(37,99,235,0.10)", "transition": "background 0.2s", "--chart-color-palette": "default"}} endpoint="/materiel/{materiel_id}/methods/verifierDispoStock/" label="verifierDispoStock" parameters={[{"name": "quantiteDemandee", "type": "any", "required": true}, {"name": "debut", "type": "any", "required": true}, {"name": "fin", "type": "any", "required": true}]} isInstanceMethod={true} instanceSourceTableId="table-materiel-5" />
        </div>
      </main>
    </div>    </div>
  );
};

export default Materiel;
