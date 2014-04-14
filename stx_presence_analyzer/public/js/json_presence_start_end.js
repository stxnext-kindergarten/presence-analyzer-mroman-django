google.load("visualization", "1", {packages:["corechart", "timeline"], 'language': 'en'});

(function($) {
    $(document).ready(function(){
        var loading = $('#loading');
        var users = [];
        $.getJSON("/api/v4/users/", function(result) {
            var dropdown = $("#user_id");
            $.each(result, function(item) {
                dropdown.append($("<option />").val(item).text(this.name).attr('data-avatar', 'avatarurl'));
            });
            users = result;
            dropdown.show();
            loading.hide();
        });
        $('#user_id').change(function(){
            var selected_user = $("#user_id").val();
            var avatar = $('#user_id').data('avatar')
            var chart_div = $('#chart_div');
            if(selected_user) {
                var newImage = users[selected_user]['avatar'];
                var user = users[selected_user]['user_id'];
                $('#avatar').children('img').attr('src', newImage);
                loading.show();
                chart_div.hide();
                $.getJSON("/api/v3/"+user, function(result) {
                    if(result.length !== undefined) {
                        $.each(result, function() {
                            this[1] = new Date(this[1] * 1000);
                            this[2] = new Date(this[2] * 1000);
                        });
                        var data = new google.visualization.DataTable();
                        data.addColumn('string', 'Weekday');
                        data.addColumn({ type: 'datetime', id: 'Start' });
                        data.addColumn({ type: 'datetime', id: 'End' });
                        data.addRows(result);
                        var options = {
                            hAxis: {title: 'Weekday'}
                        };
                        var formatter = new google.visualization.DateFormat({pattern: 'HH:mm:ss'});
                        formatter.format(data, 1);
                        formatter.format(data, 2);
                        chart_div.show();
                        loading.hide();
                        var chart = new google.visualization.Timeline(chart_div[0]);
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
