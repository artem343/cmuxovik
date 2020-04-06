// Tooltip

$('.share-cmux').tooltip({
    trigger: 'click',
    placement: 'bottom'
});

function setTooltip(btn, message) {
    $(btn).tooltip('hide')
        .attr('data-original-title', message)
        .tooltip('show');
}

function hideTooltip(btn) {
    setTimeout(function () {
        $(btn).tooltip('hide');
    }, 1000);
}

// Clipboard

var clipboard = new Clipboard('.share-cmux');

clipboard.on('success', function (e) {
    setTooltip(e.trigger, 'Ссылка скопирована :)');
    hideTooltip(e.trigger);
});

clipboard.on('error', function (e) {
    setTooltip(e.trigger, 'Не удалось скопировать :(');
    hideTooltip(e.trigger);
});