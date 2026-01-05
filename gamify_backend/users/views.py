from django.shortcuts import render

# Create your views here.

def  index(request):
    users = [
        { 'user': 'First user', 'name': 'Edwynn', 'slug': 'a-first-user'},
        { 'user': 'Second user', 'name': 'Viroen', 'slug': 'a-second-user' },
    ]
    return render(request, 'users/index.html', {
        'show_users': True,
        'users': users
    })


def user_details(request, user_slug):
    selected_user = {'title': 'A First User', 'description': 'This is the first user!'}
    return render(request, 'users/user-details.html', {
        'user_title': selected_user['title'],
        'user_description': selected_user['description']
    })