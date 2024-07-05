import flet as ft
import sqlite3


class ToDo:
    def __init__(self, page: ft.Page):
        self.page=page
        self.page.title="Tasks to Do"
        self.page.bgcolor=ft.colors.WHITE
        self.page.window.always_on_top=True
        self.page.window.height=450
        self.page.window.width=350
        self.page.window.resizable=False
        self.db_execute(query="CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, status TEXT)")
        self.all_tasks = self.db_execute(query="SELECT * FROM tasks")
        self.view="all"
        self.main()

    # Function to connect to/create Database used in the project: function to be used to manipulate it
    def db_execute(self, query, params=[]):
        with sqlite3.connect("to_do_app_database.db") as con:
            cur = con.cursor()
            cur.execute(query, params)
            con.commit()
            return cur.fetchall()


    
    # Function used to update a task
    def update_task(self, e):
        task_id = e.control.data
        task_value = e.control.value
        
        if task_value:
            self.db_execute(query='UPDATE tasks SET status = "complete" WHERE id = ?', params=[task_id])
        else:
            self.db_execute(query='UPDATE tasks SET status = "incomplete" WHERE id = ?', params=[task_id])
        
        if self.view=="all":
            self.all_tasks = self.db_execute(query="SELECT * FROM tasks")
        else:
            self.all_tasks = self.db_execute(query="SELECT * FROM tasks WHERE status = ?", params=[self.view])
        
        self.page.controls.pop()
        self.page.add(self.tasks_conteiner())
        self.page.update()



    def tasks_conteiner(self):
        return ft.Container(
            image_src='images/brasil.jpg',
            image_fit=ft.ImageFit.COVER,
            image_opacity=0.1,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Checkbox(
                                label=tsk[1],
                                value=True if tsk[2]=="complete" else False,
                                on_change=self.update_task,
                                expand=True,
                                data=tsk[0],
                                label_style=ft.TextStyle(color=ft.colors.BLACK)
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_size=20,
                                on_click=self.delete_task,
                                data=tsk[0],
                                icon_color=ft.colors.RED
                            )
                        ]
                    )
                     for tsk in self.all_tasks
                ],
                scroll=ft.ScrollMode.ALWAYS,
            ), 
            expand=True
        )


    def delete_task(self, e):
        task_id = e.control.data
        self.db_execute(query='DELETE FROM tasks WHERE id = ?', params=[task_id])
        
        if self.view=="all":
            self.all_tasks = self.db_execute(query="SELECT * FROM tasks")
        else:
            self.all_tasks = self.db_execute(query="SELECT * FROM tasks WHERE status = ?", params=[self.view])
        
        self.page.controls.pop()
        self.page.add(self.tasks_conteiner())
        self.page.update()


    def tab_view(self, e):
        if e.control.selected_index == 0:
            self.all_tasks = self.db_execute(query="SELECT * FROM tasks")
            self.view="all"
        elif e.control.selected_index == 1:
            self.all_tasks = self.db_execute(query='SELECT * FROM tasks WHERE status = "incomplete"')
            self.view="incomplete"
        elif e.control.selected_index == 2:
            self.all_tasks = self.db_execute(query='SELECT * FROM tasks WHERE status = "complete"')
            self.view="complete"
        
        self.page.controls.pop()
        self.page.add(self.tasks_conteiner())
        self.page.update()



    # MAIN PROJECT
    def main(self):
        
        # Function to add new task into the DB:
        def new_task(e):
            task_label=input_area.controls[0].value
            if task_label:
                self.db_execute(query='INSERT INTO tasks (name, status) VALUES(?, ?)', params=[task_label, "incomplete"])
                input_area.controls[0].value=""
        
                if self.view=="all":
                    self.all_tasks = self.db_execute(query="SELECT * FROM tasks")
                else:
                    self.all_tasks = self.db_execute(query="SELECT * FROM tasks WHERE status = ?", params=[self.view])
                
                self.page.controls.pop()
                self.page.add(self.tasks_conteiner())
                self.page.update()        
        

        # LAYOUT PARTS
        # Text Field and Add Button
        input_area = ft.Row(
            controls=[
                ft.TextField(
                    hint_text="Type here a taks...",
                    expand=True,
                    color=ft.colors.BLACK,
                    on_submit=new_task
                ),
                ft.FloatingActionButton(
                    icon=ft.icons.ADD,
                    mini=True,
                    on_click=new_task
                )
            ]
        )

        # Navigation Bar
        tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab("All tasks"),
                ft.Tab("In progress"),
                ft.Tab("Complete")
            ],
            on_change=self.tab_view
        )

        self.page.add(input_area, tabs, self.tasks_conteiner())

if __name__=="__main__":
    ft.app(target=ToDo, assets_dir='assets')