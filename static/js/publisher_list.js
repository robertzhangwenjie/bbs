
    $('button.edit_publisher').on('click', function () {
        var $siblingsEle = $(this).parent().siblings();
        var id = $($siblingsEle[0]).text();
        var name = $($siblingsEle[1]).text();
        var addr = $($siblingsEle[2]).text();
        $('#editModal #publisher_id').val(id);
        $('#editModal #publisher_name').val(name);
        $('#editModal #publisher_addr').val(addr);
    });
