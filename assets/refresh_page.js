// In refresh_page.js
if (!window.dash_clientside) {
    window.dash_clientside = {};
}
window.dash_clientside.clientside = {
    refresh_page: function(n_clicks) {
        if (n_clicks > 0) {
            window.location.reload();
        }
        return null;
    }
};