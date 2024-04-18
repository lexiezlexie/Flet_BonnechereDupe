import flet as ft
from typing import Callable
import pathlib
import subprocess
import time

import plotly.express as px 
from flet.plotly_chart import PlotlyChart

DEVICE_MANAGER_WIDTH = 200

class Device(ft.UserControl):
    def __init__(self, device_name, device_delete):
        super().__init__()
        self.device_name = device_name
        self.device_delete = device_delete

    def build(self):
        self.display_device = ft.Chip(
            label=ft.Text(self.device_name),
            bgcolor = ft.colors.GREEN_100,
            disabled_color = ft.colors.GREEN_200,
            on_select=self.device_clicked,
            show_checkmark = False,
        )

        self.display_view = ft.Row(
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.display_device,
                ft.IconButton(icon=ft.icons.DELETE, on_click = self.delete_clicked)

            ],
        )

        return ft.Column(controls=[self.display_view])
    
    def device_clicked(self, e):
        self.update()

    def delete_clicked(self, e):
        self.device_delete(self)

class DeviceManager(ft.UserControl):
    def build(self):
        self.new_device = ft.TextField(hint_text="Add Device?", expand=True,text_style = ft.TextStyle(color= ft.colors.WHITE))
        self.devices = ft.Column()

        # application's root control (i.e. "view") containing all other controls
        return ft.Column(
            width=DEVICE_MANAGER_WIDTH,
            controls=[
                ft.Row(
                    controls=[
                        self.new_device,
                        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked),
                    ],
                ),
                self.devices,
            ],
        )

    def add_clicked(self, e):
        device = Device(self.new_device.value, self.device_delete)
        self.devices.controls.append(device)
        self.new_device.value =""
        self.update()

    def device_delete(self, device):
        self.devices.controls.remove(device)
        self.update()

    def update(self):
        super().update()

class Launch_Button(ft.UserControl):
    def build(self):
        return ft.Container(
            alignment=ft.alignment.center,
            height = 45,
            content = ft.Row(
                alignment = ft.MainAxisAlignment.END,
                vertical_alignment = ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.ElevatedButton(
                        text = "New File",
                        on_click=self.open_vscode_file
                    ),
                ],
            )
        )
    
    def open_vscode_file(self, e):
        try:
            subprocess.call(["code", "test.py"])
        except Exception as e:
            print(f"file failed to open: {e}")

class SingleLine(ft.UserControl):
    def __init__(self, line_count, add_line):
        super().__init__()
        self.line_count = line_count
        self.add_line = add_line

    def build(self):
        print(f"line count = {self.line_count}")
        return  ft.Row(
            controls=[
                ft.Text(
                    str(self.line_count),
                    color = ft.colors.WHITE,
                    bgcolor = ft.colors.GREEN_600,
                ),
                ft.TextField(
                    text_style = ft.TextStyle(color= ft.colors.WHITE),
                    multiline=False,  # True means: it will be possible to have many lines of text
                    expand=False,  # tells the field to 'expand' (take all the available space)
                    border_color=ft.colors.TRANSPARENT,
                    # on_submit = self.add_line, # makes the border of the field transparent(invisible), creating an immersive effect
                ),
            ],
        ),

class SampleGraph(ft.UserControl):
    def build(self):
        df = px.data.gapminder().query("continent == 'Oceania'")
        fig = px.line(
            df,
            x="year",
            y="pop",
            hover_data=["lifeExp", "gdpPercap"],
            color="country",
            labels={"pop": "population of Canada"},
            height=400,
        )

        return ft.Container(
            content = PlotlyChart(fig, expand = True)
        )

class CodeEditor(ft.UserControl):

    def build(self):

        # application's root control (i.e. "view") containing all other controls
        self.number_of_lines = 1
        self.line_counts = ft.Column()
        self.line_counts.controls.append(self.add_line_numbering(str(self.number_of_lines)))
        
        self.editor = ft.TextField(
                    text_style = ft.TextStyle(color= ft.colors.WHITE),
                    multiline=True,  # True means: it will be possible to have many lines of text
                    expand=False,  # tells the field to 'expand' (take all the available space)
                    border_color=ft.colors.TRANSPARENT,
                    on_change = self.count_line,
        )

        return ft.Container(
            width = 900,
            height = 600,
            bgcolor = ft.colors.GREY_700,
            content = 
                ft.Column(
                    width=DEVICE_MANAGER_WIDTH,
                    scroll = ft.ScrollMode.ADAPTIVE,
                    spacing = 0,
                    controls = [
                        ft.Row(
                            controls=[
                                self.line_counts,
                                self.editor,
                            ],
                        ),
                    ],
                ),
        )
    
    def add_line_numbering(self, line_count:str):
        return ft.Text(
            line_count,
            color = ft.colors.WHITE,
            bgcolor = ft.colors.GREY_800,)

    def count_line(self, e):
        number_of_lines = len(self.editor.value.splitlines())
        if  number_of_lines > self.number_of_lines:
            self.number_of_lines += 1
            self.line_counts.controls.append(self.add_line_numbering(str(self.number_of_lines)))
            
        if number_of_lines < self.number_of_lines:
            self.number_of_lines -= 1
            self.line_counts.controls.pop()
            
        self.update()
            
        print(f"number of lines: {number_of_lines}")

    # def add_line(self,e):
    #     self.line_count += 1
    #     print("add line called")
    #     line = SingleLine(self.line_count, self.add_line)
    #     self.lines.controls.append(line)
    #     self.update()

    def update(self):
        super().update()


class PlottingButton(ft.UserControl):

    def make_chip(self, chip_name):
        return ft.Chip(
            label=ft.Text(chip_name),
            bgcolor = ft.colors.GREY_500,
            selected_color = ft.colors.GREY_700,
            on_select=self.device_clicked,
            show_checkmark = False,
            )

    def device_clicked(self, e):
        super().update()

    def build(self):

        start_plotting = self.make_chip("Start Plotting")
        clear_plot = self.make_chip("Clear Plot")
        calibrate = self.make_chip("Calibrate")

        return ft.Column(
            controls = [
                ft.Container (
                    padding = ft.padding.only(top = 10),
                    content =
                        ft.Row(
                            alignment = ft.MainAxisAlignment.CENTER,
                            vertical_alignment="center",
                            controls=[
                                start_plotting,
                                clear_plot,
                                calibrate,
                            ],
                        ),
                )
            ],
        )
    
class DragBlock(ft.UserControl):
    def drag(self, e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()

    def new_card(self):
        return ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=5,
        on_pan_update=self.drag,
        left=0,
        top=0,
        content=ft.Container(bgcolor=ft.colors.GREEN, width=70, height=100),
        )
    
    def build(self):
        card = self.new_card()

        return ft.Stack(controls = [card,],  width = 1000, height = 500)



class MainPage(ft.UserControl):
    def build(self):

        launch_button = Launch_Button()
        text_editor = CodeEditor()
        plotting_buttons = PlottingButton()
        self.dragging_card = DragBlock()


        return ft.Tabs(
            divider_color = ft.colors.AMBER,
            indicator_color = ft.colors.AMBER,
            unselected_label_color = ft.colors.WHITE,
            label_color = ft.colors.AMBER,
            indicator_tab_size = True,
            indicator_thickness = 10,
            overlay_color = {
                ft.MaterialState.FOCUSED:ft.colors.AMBER,
                ft.MaterialState.HOVERED:ft.colors.with_opacity(0.3, ft.colors.WHITE),
                ft.MaterialState.DEFAULT: ft.colors.GREY_700,
            },
            selected_index=0,
            animation_duration = 300,
            tabs=[
                ft.Tab(
                    text="Raw",
                    content=ft.Container(
                        content=ft.Column(
                            controls = [
                                plotting_buttons,
                                SampleGraph(),
                            ],
                        ),
                        alignment=ft.alignment.center,
                    ),
                ),
                ft.Tab(
                    text = "Processed",
                    content = ft.Container(
                        content=ft.Text("This is Tab 2"),
                        alignment=ft.alignment.center,
                    ),
                ),
                ft.Tab(
                    text="Config",
                    content= ft.Container(
                        content = ft.Column(
                            controls = [
                                ft.Row(
                                    controls = [
                                        launch_button,
                                    ]
                                ),
                                text_editor,
                            ],
                            scroll="hidden",
                        )
                    ),
                ),
            #     ft.Tab(
            #         text="Automation Framework",
            #         content= ft.Column(
            #             contorls = [
            #                 ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_card),
            #                 ft.Container(
            #                     content=self.dragging_card,
            #                     alignment=ft.alignment.center,
            #                     ),
            #             ]
            #         ),
            #     ),
            # ],
                ft.Tab(
                    text="Automation Framework",
                    content= ft.Container(
                        content=self.dragging_card,
                        alignment=ft.alignment.center,
                        ),
                    ),
            ],
            expand=1,
        )
    
    def add_card(self, e):
        card = DragBlock.new_card()
        self.dragging_card.controls.append(card)
        super().update()


def main(page: ft.Page):
    page.title = "Bonnechere Dupe"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()
    page.bgcolor = ft.colors.GREY_900

    # create application instance
    device_manager = DeviceManager()
    main_page = MainPage()

    # add application's root control to the page
    page.add(
        ft.Row(
            [
                device_manager,
                ft.VerticalDivider(),
                ft.Container(
                    width = 1000,
                    # bgcolor=ft.colors.GREY_800,
                    alignment=ft.alignment.center,
                    content = main_page
                    ),
            ],
            spacing = 0,
            expand = True,
        )
    )

ft.app(target=main)