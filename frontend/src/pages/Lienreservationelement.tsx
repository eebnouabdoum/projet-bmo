import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";

const Lienreservationelement: React.FC = () => {
  return (
    <div id="page-lienreservationelement-7">
    <div id="i6faur" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="i7ya57" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="id6jxq" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="iq4yfi" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="ifw1mj" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/centrecongres">{"CentreCongres"}</a>
          <a id="i69rdx" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/elementcentre">{"ElementCentre"}</a>
          <a id="iptt7u" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/indisponibilite">{"Indisponibilite"}</a>
          <a id="i47wjj" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/tarifsaisonnier">{"TarifSaisonnier"}</a>
          <a id="ieb89l" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reservation">{"Reservation"}</a>
          <a id="iw2pdn" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/materiel">{"Materiel"}</a>
          <a id="is7m4c" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestation">{"Prestation"}</a>
          <a id="igal3r" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/lienreservationelement">{"LienReservationElement"}</a>
          <a id="ir047i" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/lienreservationmateriel">{"LienReservationMateriel"}</a>
          <a id="igo5qf" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/lienreservationprestation">{"LienReservationPrestation"}</a>
        </div>
        <p id="i0uvnl" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="ilg91q" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="ih9xhl" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"LienReservationElement"}</h1>
        <p id="iqti26" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage LienReservationElement data"}</p>
        <TableBlock id="table-lienreservationelement-7" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="LienReservationElement List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Id", "column_type": "field", "field": "id", "type": "str", "required": true}, {"label": "CoutCalcule", "column_type": "field", "field": "coutCalcule", "type": "float", "required": true}, {"label": "Concerne", "column_type": "lookup", "path": "concerne", "entity": "Reservation", "field": "id", "type": "str", "required": true}, {"label": "Cible", "column_type": "lookup", "path": "Cible", "entity": "ElementCentre", "field": "id", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "id", "label": "id", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "coutCalcule", "label": "coutCalcule", "type": "float", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "concerne", "field": "concerne", "lookup_field": "nomContact", "entity": "Reservation", "type": "str", "required": true}, {"column_type": "lookup", "path": "Cible", "field": "Cible", "lookup_field": "id", "entity": "ElementCentre", "type": "str", "required": true}]}} dataBinding={{"entity": "LienReservationElement", "endpoint": "/lienreservationelement/"}} />
        <div id="iygq4l" style={{"marginTop": "20px", "display": "flex", "gap": "10px", "flexWrap": "wrap", "--chart-color-palette": "default"}}>
          <MethodButton id="i57ntl" className="action-button-component" style={{"display": "inline-flex", "alignItems": "center", "padding": "6px 14px", "background": "linear-gradient(90deg, #2563eb 0%, #1e40af 100%)", "color": "#fff", "textDecoration": "none", "borderRadius": "4px", "fontSize": "13px", "fontWeight": "600", "letterSpacing": "0.01em", "cursor": "pointer", "border": "none", "boxShadow": "0 1px 4px rgba(37,99,235,0.10)", "transition": "background 0.2s", "--chart-color-palette": "default"}} endpoint="/lienreservationelement/{lienreservationelement_id}/methods/calculerCoutLien/" label="calculerCoutLien" parameters={[{"name": "duree", "type": "any", "required": true}]} isInstanceMethod={true} instanceSourceTableId="table-lienreservationelement-7" />
        </div>
      </main>
    </div>    </div>
  );
};

export default Lienreservationelement;
