import flet as ft
import sqlite3
from airtable import *

class ToDo:
    def __init__(self, page: ft.Page):
        self.page=page
        self.page.title="Tasks to Do"
        self.page.bgcolor=ft.colors.WHITE
        self.page.window.always_on_top=True
        self.page.window.height=450
        self.page.window.width=350
        self.page.window.resizable=False
        self.page.adaptive=True
        self.all_tasks = get_Records()
        self.view="all"
        self.main()

    
    
    
    # Function to connect to/create Database used in the project: function to be used to manipulate it
    def db_execute(self, query, params=[]):
        with sqlite3.connect("assets/db/to_do_app_database.db") as con:
            cur = con.cursor()
            cur.execute(query, params)
            con.commit()
            return cur.fetchall()


    
    # Function used to update a task
    def update_task(self, e):
        task_id = e.control.data
        task_value = e.control.value
        
        if task_value:
            update_Record(id=task_id, content={"Status": "complete"})
        else:
            update_Record(id=task_id, content={"Status": "incomplete"})
        
        if self.view=="all":
            self.all_tasks = get_Records()
        else:
            self.all_tasks = get_Records(self.view)
        
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
                                label=tsk.get("Name"),
                                value=True if tsk.get("Status")=="complete" else False,
                                on_change=self.update_task,
                                expand=True,
                                data=tsk.get("ID"),
                                label_style=ft.TextStyle(color=ft.colors.BLACK)
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_size=20,
                                on_click=self.delete_task,
                                data=tsk.get("ID"),
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
        delete_Record(task_id)
        
        if self.view=="all":
            self.all_tasks = get_Records()
        else:
            self.all_tasks = get_Records(self.view)
        
        self.page.controls.pop()
        self.page.add(self.tasks_conteiner())
        self.page.update()


    def tab_view(self, e):
        if e.control.selected_index == 0:
            self.all_tasks = get_Records()
            self.view="all"
        elif e.control.selected_index == 1:
            self.all_tasks = get_Records("incomplete")
            self.view="incomplete"
        elif e.control.selected_index == 2:
            self.all_tasks = get_Records("complete")
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
                create_Record({"Name": task_label, "Status": "incomplete"})
                input_area.controls[0].value=""
                input_area.controls[0].autofocus=True
        
                if self.view=="all":
                    self.all_tasks = get_Records()
                else:
                    self.all_tasks = get_Records(self.view)
                
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
                    on_submit=new_task,
                    max_length=20,
                    capitalization=ft.TextCapitalization.SENTENCES,
                    autofocus=True
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