# Web Task Management: Collaborative Project Management for Remote Teams
The project curently is coming to an end.

I created a web-based platform: a system that manages tasks in remote teams, facilitating effective collaboration on projects. Real-time task assignment, priority tracking and role-based access control were implemented. The platform allows the Owner to oversee every element in the team, designates leaders to manage projects. Project leaders oversee the team's progress. There is also constant communication thanks to shared emails. The process of deploying team members is based on invitations.

## SETUP

1. First, clone the repository.
2. Next, run 
    On windows:
    'python manage.py runserver',
    On macOS or Linux:
    'python3 manage.py runserver'

## PROJECT

### Registration, Login

![Registration](./images/Register.png)
![Login](./images/login.png)


### Notification

![Login](./images/Notification.png)
We get a notification when we are invited to join a team, when we are assigned to a task

- Task deadline reminder notifications coming soon

### Team Members

![TeamMembers](./images/LIST.png)
![TeamMembersProfile](./images/EditProfile.png)

We can see our team, we can see if a team member is active and there is also the possibility to see the person's team profile, by sharing emails we can keep in touch. You can also see the responsibilities, the owner can edit team profiles and also give the manager to someone

### Projects

![ProjectBoard](./images/ProjectBoard.png)
![ProjectBoard](./images/2023-11-13(8).png)

On the project board we can see all projects, the progress of the project leader as well as the project priority, at the top of the page we can see the number of all projects, completed projects as well as projects in progress. 
Owner can create projects and appoint leaders.

On the project page, there is a title, a description of the project. The leader can create tasks and assign them to team members. There is also an Activity sector, where you can see the activity of team members.

Sorting (asc desc) by date, name-alphabetical, progress, search by name and by priority is available.

- improved image of the activity sector, and more features in the activity sector coming soon

### Tasks

![ProjectBoard](./images/TaskBoard.png)
![ProjectBoard](./images/2023-11-13(9).png)

On the task board it is possible to see who is assigned to a task, what the progress is, what the priority is and also which project the task belongs to.
At the top of the page we can see the number of all tasks, completed tasks as well as tasks in progress.
Sorting (asc desc) by date, name-alphabetical, progress, search by name and by priority is available.

On the task page the user can add attachments, there is also a comments section where the leader can comment on the user's work


- Better view of the tasks page, and a view of the number of completed and progressing tasks in the near future

###
- Setting page for team and user, home page with all shortcuts and reminders, my task and my project page with shortcuts, team home page coming soon.

## License

This project is licensed under the [MIT License](LICENSE).