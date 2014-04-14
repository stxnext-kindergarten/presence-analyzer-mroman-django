function parseInterval(value) {
    var result = new Date(1,1,1);
    result.setMilliseconds(value*1000);
    return result;
}

(function($) {
    $(document).ready(function(){
        var loading = $('#loading');
        var users = [];
        $.getJSON("/api/v4/users/", function(result) {
            var dropdown = $("#user_id");
            $.each(result, function(item) {
                dropdown.append($("<option />").val(item).text(this.name).attr('data-avatar', this.avatar));
            });
            users = result;
            dropdown.show();
            loading.hide();
        });
        $('#user_id').change(function(){
            var selected_user = $("#user_id").val();
            var avatar = $('#user_id').data('avatar');
            var chart_div = $('#chart_div');
            if(selected_user) {
                var newImage = users[selected_user]['avatar'];
                var user = users[selected_user]['user_id'];
                $('#avatar').children('img').attr('src', newImage);
                loading.show();
                chart_div.hide();
                $.getJSON("/api/v2/"+user, function(result) {
                    if (result.length !== undefined) {
                        $.each(result, function(index, value) {
                        value[1] = parseInterval(value[1]);
                        });
                        var data = new google.visualization.DataTable();
                        data.addColumn('string', 'Weekday');
                        data.addColumn('datetime', 'Mean time (h:m:s)');
                        data.addRows(result);
                        var options = {
                            hAxis: {title: 'Weekday'}
                        };
                        var formatter = new google.visualization.DateFormat({pattern: 'HH:mm:ss'});
                        formatter.format(data, 1);

                        chart_div.show();
                        loading.hide();
                        var chart = new google.visualization.ColumnChart(chart_div[0]);
                        chart.draw(data, options);
                    }
                    else{
                        chart_div.show();
                        $('#chart_div').text('Brak danych dla tego użytkownika');
                        loading.hide();
                    }
                });
            }
        });
    });
})(jQuery);
