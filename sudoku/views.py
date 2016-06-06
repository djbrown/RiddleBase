from django.http import Http404, JsonResponse
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from sudoku.models import Sudoku


def index(request) -> HttpResponse:
    return render(request, 'sudoku/index.html', {
        'ids': list(sudoku.id for sudoku in Sudoku.objects.all()),
    })


def riddle(request: HttpRequest, riddle_id: int) -> HttpResponse:
    try:
        sudoku = Sudoku.objects.get(pk=riddle_id)
    except Sudoku.DoesNotExist:
        raise Http404("Sudoku does not exist")

    context = sudoku.get_context(request.user)
    context.update({
        'box_rows': sudoku.box_rows,
    })
    return render(request, 'sudoku/riddle.html', context)


@csrf_exempt
@require_POST
def check(request: HttpRequest, riddle_id: int) -> JsonResponse:
    try:
        sudoku = Sudoku.objects.get(pk=riddle_id)
    except Sudoku.DoesNotExist:
        raise Http404("Sudoku does not exist")

    proposal = request.POST.get("proposal")
    correct = proposal is not None and proposal == sudoku.solution
    response = {'correct': correct}
    return JsonResponse(response)


def creator(request: HttpRequest) -> HttpResponse:
    return render(request, 'sudoku/creator.html')


@require_POST
def create(request: HttpRequest) -> JsonResponse:
    error = []
    if not request.user.has_perm("riddles.add_sudoku"):
        error.append("no permission")

    solution = request.POST.get("solution")
    pattern = request.POST.get("pattern")

    if solution is None:
        error.append("no solution")
    if pattern is None:
        error.append("no pattern")

    if error:
        return JsonResponse({'error': error})

    created = Sudoku(solution=solution,
                     pattern=pattern,
                     state=pattern,
                     difficulty=5,
                     box_rows=3)
    created.save()
    return JsonResponse({'id': created.id})
