$(document).ready(function(){

    function crsort(val_1, val_2) {
            const ord = ['1/8','1/4','1/2','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30'];
            var v1 = ord.indexOf(val_1);
            var v2 = ord.indexOf(val_2);
            if (v1 < v2) {
                return -1;
            } else if (v1 > v2) {
              return 1;
            } else {
              return 0;
            }
          };

    $.fn.dataTable.type("cr", {
        order: {
            asc: function (a, b) {
                return crsort(a,b)

            },
            desc: function (a, b) {
                return crsort(b,a);
            },
        },
        className: "cr-sort",
    });



    new DataTable('#cs', { order: [[2, 'asc']], columnDefs: [{type: 'natural', targets:2},{type: 'cr', targets:1}]})
    new DataTable('#setTable', { order: [[2, 'asc']], columnDefs: [{type: 'natural', targets:0}],
                'rowCallback': function(row, data, index){
                                if (data[1] == 'Yes'){
                                                $('td', row).css('color', '#7CFC00')
                                }
                }


        })
    $(".dt-container").each(function(){
                $(this).hide()
    });
    $("#cs_wrapper").show()
    $("#col").change(function() {

                $(".dt-container").each(function(){
                                $(this).hide()
                });
                $('#' + $(this).val()+ '_wrapper').show()
    });

});
