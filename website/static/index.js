function deleteRoute(routeId){
    fetch('/delete-route', {
        method: 'POST',
        body: JSON.stringify({ routeId: routeId}),
    }).then((_res) => {
        window.location.href = "/";
    });
}