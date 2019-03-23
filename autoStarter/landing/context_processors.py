from landing.models import TopMenuPoint


def getting_top_menu_points(request):
    main_points = TopMenuPoint.objects.all()
    if len(main_points) > 3:
        main_points = main_points[:3]

        drop_points = TopMenuPoint.objects.all()
        drop_points = drop_points[3:]
    else:
        drop_points = []

    context = {
        'main_points': main_points,
        'drop_points': drop_points,
    }

    return context