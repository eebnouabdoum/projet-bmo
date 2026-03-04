import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";

const Tarifsaisonnier: React.FC = () => {
  return (
    <div id="page-tarifsaisonnier-3">
    <div id="ilviym" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="i2tdmx" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="i5jhak" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="ivfemh" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="igw8su" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/centrecongres">{"CentreCongres"}</a>
          <a id="i2gb5t" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/elementcentre">{"ElementCentre"}</a>
          <a id="i2gkoi" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/indisponibilite">{"Indisponibilite"}</a>
          <a id="i8nvin" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/tarifsaisonnier">{"TarifSaisonnier"}</a>
          <a id="itty9h" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reservation">{"Reservation"}</a>
          <a id="ihpz0i" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/materiel">{"Materiel"}</a>
          <a id="iqxvlk" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestation">{"Prestation"}</a>
          <a id="ixxkd1" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/lienreservationelement">{"LienReservationElement"}</a>
          <a id="is4yoa" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/lienreservationmateriel">{"LienReservationMateriel"}</a>
          <a id="i90equ" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/lienreservationprestation">{"LienReservationPrestation"}</a>
        </div>
        <p id="i993o5" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="i3fx07" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="ilztfl" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"TarifSaisonnier"}</h1>
        <p id="igq81l" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage TarifSaisonnier data"}</p>
        <TableBlock id="table-tarifsaisonnier-3" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="TarifSaisonnier List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Id", "column_type": "field", "field": "id", "type": "str", "required": true}, {"label": "Saison", "column_type": "field", "field": "saison", "type": "enum", "options": ["BASSE", "HAUTE", "MOYENNE"], "required": true}, {"label": "PrixJournalier", "column_type": "field", "field": "prixJournalier", "type": "float", "required": true}, {"label": "Possede", "column_type": "lookup", "path": "possede", "entity": "ElementCentre", "field": "id", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "id", "label": "id", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "saison", "label": "saison", "type": "enum", "required": true, "defaultValue": null, "options": ["BASSE", "HAUTE", "MOYENNE"]}, {"column_type": "field", "field": "prixJournalier", "label": "prixJournalier", "type": "float", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "possede", "field": "possede", "lookup_field": "id", "entity": "ElementCentre", "type": "str", "required": true}]}} dataBinding={{"entity": "TarifSaisonnier", "endpoint": "/tarifsaisonnier/"}} />
        <div id="inkq1t" style={{"marginTop": "20px", "display": "flex", "gap": "10px", "flexWrap": "wrap", "--chart-color-palette": "default"}}>
          <MethodButton id="iaszxd" className="action-button-component" style={{"display": "inline-flex", "alignItems": "center", "padding": "6px 14px", "background": "linear-gradient(90deg, #2563eb 0%, #1e40af 100%)", "color": "#fff", "textDecoration": "none", "borderRadius": "4px", "fontSize": "13px", "fontWeight": "600", "letterSpacing": "0.01em", "cursor": "pointer", "border": "none", "boxShadow": "0 1px 4px rgba(37,99,235,0.10)", "transition": "background 0.2s", "--chart-color-palette": "default"}} endpoint="/tarifsaisonnier/{tarifsaisonnier_id}/methods/getPrixPourDate/" label="getPrixPourDate" parameters={[{"name": "dateCible", "type": "any", "required": true}]} isInstanceMethod={true} instanceSourceTableId="table-tarifsaisonnier-3" />
        </div>
      </main>
    </div>    </div>
  );
};

export default Tarifsaisonnier;
