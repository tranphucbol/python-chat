$(document).ready(function(){
    function showMessage() {
        var params = new window.URLSearchParams(window.location.search);
        if(params.get('message') !== null) {
            $('body').prepend(`
                <div class="p-3" style="position: absolute; top: 0; right: 0; z-index: 1000">

                <!-- Then put toasts within -->
                    <div class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-delay="5000">
                        <div class="toast-header">
                            <i class="fas fa-exclamation-circle text-danger"></i>
                            <strong class="ml-2 mr-auto text-danger">Error</strong>
                            <small class="text-muted">just now</small>
                            <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="toast-body">
                            ${params.get('message')}
                        </div>
                    </div>
                </div>
            `);
            $('.toast').toast('show');
        }
    }

    showMessage();
});