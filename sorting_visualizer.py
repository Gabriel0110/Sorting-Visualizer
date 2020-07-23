import arcade
from arcade.gui import *
import random
import time

SCREEN_WIDTH = 1275
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Sorting Visualizer"

game = None
sorting = False

def getButtonThemes():
    theme = Theme()
    theme.set_font(24, arcade.color.BLACK)
    normal = "images/Normal.png"
    hover = "images/Hover.png"
    clicked = "images/Clicked.png"
    locked = "images/Locked.png"
    theme.add_button_textures(normal, hover, clicked, locked)
    return theme

class Shape:
    """ Generic base shape class """
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.area = self.width * self.height
        self.shape_list = None

    def draw(self):
        self.shape_list.center_x = self.x
        self.shape_list.center_y = self.y
        self.shape_list.draw()

class AddBarsButton(TextButton):
    def __init__(self, view, x=0, y=0, width=250, height=40, text="New Bars", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)

    def on_press(self):
        global game
        game.addBars()

class ResetBarsButton(TextButton):
    def __init__(self, view, x=0, y=0, width=250, height=40, text="Reset Bars", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)

    def on_press(self):
        global game
        game.resetBars()

class QuickSortButton(TextButton):
    def __init__(self, view, x=0, y=0, width=250, height=40, text="Quick Sort", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)

    def on_press(self):
        global game
        game.QuickSort()

class MergeSortButton(TextButton):
    def __init__(self, view, x=0, y=0, width=250, height=40, text="Merge Sort", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)

    def on_press(self):
        global game
        game.MergeSort()

class BubbleSortButton(TextButton):
    def __init__(self, view, x=0, y=0, width=250, height=40, text="Bubble Sort", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)

    def on_press(self):
        global game
        game.BubbleSort()

class HeapSortButton(TextButton):
    def __init__(self, view, x=0, y=0, width=250, height=40, text="Heap Sort", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)

    def on_press(self):
        global game
        game.HeapSort()

class InsertionSortButton(TextButton):
    def __init__(self, view, x=0, y=0, width=250, height=40, text="Insertion Sort", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)

    def on_press(self):
        global game
        game.InsertionSort()

class SelectionSortButton(TextButton):
    def __init__(self, view, x=0, y=0, width=250, height=40, text="Selection Sort", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)

    def on_press(self):
        global game
        game.SelectionSort()

class ToggleAnimationButton(TextButton):
    def __init__(self, view, x=0, y=0, width=250, height=40, text="Animation On/Off", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)

    def on_press(self):
        global game
        if game.animate == True:
            game.animate = False
        else:
            game.animate = True

class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.GRAY)

        self.theme = getButtonThemes()
        self.button_list.append(AddBarsButton(self, SCREEN_WIDTH*0.25, SCREEN_HEIGHT*0.075, 300, 40, "New Bars", theme=self.theme))
        self.button_list.append(ResetBarsButton(self, SCREEN_WIDTH*0.75, SCREEN_HEIGHT*0.075, 300, 40, "Reset Bars", theme=self.theme))
        self.button_list.append(ToggleAnimationButton(self, SCREEN_WIDTH*0.9, SCREEN_HEIGHT*0.9, 283, 40, "Animation On/Off", theme=self.theme))
        self.button_list.append(QuickSortButton(self, SCREEN_WIDTH*0.9, SCREEN_HEIGHT*0.7, 250, 40, "Quick Sort", theme=self.theme))
        #self.button_list.append(MergeSortButton(self, SCREEN_WIDTH*0.9, SCREEN_HEIGHT*0.6, 250, 40, "Merge Sort", theme=self.theme))
        self.button_list.append(BubbleSortButton(self, SCREEN_WIDTH*0.9, SCREEN_HEIGHT*0.6, 250, 40, "Bubble Sort", theme=self.theme))
        self.button_list.append(HeapSortButton(self, SCREEN_WIDTH*0.9, SCREEN_HEIGHT*0.5, 250, 40, "Heap Sort", theme=self.theme))
        self.button_list.append(InsertionSortButton(self, SCREEN_WIDTH*0.9, SCREEN_HEIGHT*0.4, 250, 40, "Insertion Sort", theme=self.theme))
        self.button_list.append(SelectionSortButton(self, SCREEN_WIDTH*0.9, SCREEN_HEIGHT*0.3, 250, 40, "Selection Sort", theme=self.theme))

        self.all_sprites = None
        self.bar_list = None
        self.presorted_bars = None
        self.max_bars = 15
        self.current_bars = 0
        self.bar_positions = {}

        self.sort_time = 0.0

        self.animate = False

        self.setup()

    def setup(self):
        self.bar_list = []

    def on_draw(self):
        arcade.start_render()

        for bar in self.bar_list:
            bar.draw()

        arcade.draw_text("Animations: {}".format("ON" if self.animate == True else "OFF"), SCREEN_WIDTH*0.9, SCREEN_HEIGHT*0.83, arcade.color.WHITE, font_size=20, font_name='GOTHIC', anchor_x="center", bold=True)
        
        if self.animate == False:
            arcade.draw_text("Sort time: {:.3f} seconds".format(self.sort_time), SCREEN_WIDTH/2, SCREEN_HEIGHT*0.01, arcade.color.WHITE, font_size=20, font_name='GOTHIC', anchor_x="center", bold=True)

        for button in self.button_list:
            button.draw()

    def addBars(self):
        import copy
        self.sort_time = 0.0
        width = 10
        inc = 0.02

        if len(self.bar_list) > 0:
            del self.bar_list[:]

        for i in range(56):
            height = random.randint(5, 650)
            red = random.randint(1, 256)
            green = random.randint(1, 256)
            blue = random.randint(1, 256)
            alpha = 255
            bar = Bar(800*inc, SCREEN_HEIGHT*0.28, width, height, (red, green, blue, alpha))
            self.bar_list.append(bar)
            inc += 0.01

        self.presorted_bars = self.bar_list[:]

    def resetBars(self):
        #del self.bar_list[:]
        self.bar_list = self.presorted_bars

    def QuickSort(self):
        global game

        def partition(arr,low,high):
            i = (low-1)
            pivot = arr[high] 
        
            if self.animate == True:
                for j in range(low , high):
                    if arr[j] <= pivot:
                        i = i+1
                        arr[i],arr[j] = arr[j],arr[i]

                        arcade.start_render()
                        # "SWAP" BARS
                        bar_i = self.bar_list[i]
                        bar_j = self.bar_list[j]
                        new_bar_i = Bar(bar_j.x, SCREEN_HEIGHT*0.28, bar_i.width, bar_i.height, bar_i.color)
                        new_bar_j = Bar(bar_i.x, SCREEN_HEIGHT*0.28, bar_j.width, bar_j.height, bar_j.color)
                        del self.bar_list[i]
                        self.bar_list.insert(i, new_bar_j)
                        del self.bar_list[j]
                        self.bar_list.insert(j, new_bar_i)
                        for bar in self.bar_list:
                            bar.draw()
            
                arr[i+1],arr[high] = arr[high],arr[i+1]

                # "SWAP" BARS
                bar_i1 = self.bar_list[i+1]
                bar_high = self.bar_list[high]
                new_bar_i1 = Bar(bar_high.x, SCREEN_HEIGHT*0.28, bar_i1.width, bar_i1.height, bar_i1.color)
                new_bar_high = Bar(bar_i1.x, SCREEN_HEIGHT*0.28, bar_high.width, bar_high.height, bar_high.color)
                del self.bar_list[i+1]
                self.bar_list.insert(i+1, new_bar_high)
                del self.bar_list[high]
                self.bar_list.insert(high, new_bar_i1)
                for bar in self.bar_list:
                    bar.draw()
                time.sleep(0.5)
                arcade.finish_render()
            else:
                for j in range(low , high):
                    if arr[j] <= pivot:
                        i = i+1
                        arr[i],arr[j] = arr[j],arr[i]

                        # "SWAP" BARS
                        bar_i = self.bar_list[i]
                        bar_j = self.bar_list[j]
                        new_bar_i = Bar(bar_j.x, SCREEN_HEIGHT*0.28, bar_i.width, bar_i.height, bar_i.color)
                        new_bar_j = Bar(bar_i.x, SCREEN_HEIGHT*0.28, bar_j.width, bar_j.height, bar_j.color)
                        del self.bar_list[i]
                        self.bar_list.insert(i, new_bar_j)
                        del self.bar_list[j]
                        self.bar_list.insert(j, new_bar_i)
            
                arr[i+1],arr[high] = arr[high],arr[i+1]

                # "SWAP" BARS
                bar_i1 = self.bar_list[i+1]
                bar_high = self.bar_list[high]
                new_bar_i1 = Bar(bar_high.x, SCREEN_HEIGHT*0.28, bar_i1.width, bar_i1.height, bar_i1.color)
                new_bar_high = Bar(bar_i1.x, SCREEN_HEIGHT*0.28, bar_high.width, bar_high.height, bar_high.color)
                del self.bar_list[i+1]
                self.bar_list.insert(i+1, new_bar_high)
                del self.bar_list[high]
                self.bar_list.insert(high, new_bar_i1)

            return (i+1)

        def quickSort(arr,low,high):
            if low < high:
                pi = partition(arr,low,high)
                quickSort(arr, low, pi-1)
                quickSort(arr, pi+1, high)

        self.presorted_bars = self.bar_list[:]
        areas = [bar.area for bar in self.bar_list]
        start_time = time.time()
        quickSort(areas, 0, len(areas)-1)
        self.sort_time = time.time() - start_time
        print("QuickSort time: {} seconds".format(str(self.sort_time)))

    def BubbleSort(self):
        global game
        
        def bubbleSort(areas):
            swapped = True
            while swapped:
                swapped = False
                for i in range(len(areas) - 1):
                    if areas[i] > areas[i + 1]:
                        areas[i], areas[i + 1] = areas[i + 1], areas[i]

                        if self.animate == True:
                            arcade.start_render()
                            # "SWAP" BARS
                            bar_i = self.bar_list[i]
                            bar_i1 = self.bar_list[i+1]
                            new_bar_i = Bar(bar_i1.x, SCREEN_HEIGHT*0.28, bar_i.width, bar_i.height, bar_i.color)
                            new_bar_i1 = Bar(bar_i.x, SCREEN_HEIGHT*0.28, bar_i1.width, bar_i1.height, bar_i1.color)
                            del self.bar_list[i]
                            self.bar_list.insert(i, new_bar_i1)
                            del self.bar_list[i+1]
                            self.bar_list.insert(i+1, new_bar_i)
                            for bar in self.bar_list:
                                bar.draw()
                            time.sleep(0.15)
                            arcade.finish_render()
                            # Set the flag to True so we'll loop again
                            swapped = True
                        else:
                            # "SWAP" BARS
                            bar_i = self.bar_list[i]
                            bar_i1 = self.bar_list[i+1]
                            new_bar_i = Bar(bar_i1.x, SCREEN_HEIGHT*0.28, bar_i.width, bar_i.height, bar_i.color)
                            new_bar_i1 = Bar(bar_i.x, SCREEN_HEIGHT*0.28, bar_i1.width, bar_i1.height, bar_i1.color)
                            del self.bar_list[i]
                            self.bar_list.insert(i, new_bar_i1)
                            del self.bar_list[i+1]
                            self.bar_list.insert(i+1, new_bar_i)
                            swapped = True

        self.presorted_bars = self.bar_list[:]
        areas = [bar.area for bar in self.bar_list]
        bar_dict = {bar.area:bar for bar in self.bar_list}
        start_time = time.time()
        bubbleSort(areas)
        self.sort_time = time.time() - start_time
        print("BubbleSort time: {} seconds".format(str(self.sort_time)))

    def HeapSort(self):
        global game
        
        def heapify(areas, heap_size, root_index):
            # Assume the index of the largest element is the root index
            largest = root_index
            left_child = (2 * root_index) + 1
            right_child = (2 * root_index) + 2

            # If the left child of the root is a valid index, and the element is greater
            # than the current largest element, then update the largest element
            if left_child < heap_size and areas[left_child] > areas[largest]:
                largest = left_child

            # Do the same for the right child of the root
            if right_child < heap_size and areas[right_child] > areas[largest]:
                largest = right_child

            # If the largest element is no longer the root element, swap them
            if largest != root_index:
                areas[root_index], areas[largest] = areas[largest], areas[root_index]
                if self.animate == False:
                    # "SWAP" BARS
                    bar_root = self.bar_list[root_index]
                    bar_largest = self.bar_list[largest]
                    new_bar_root = Bar(bar_largest.x, SCREEN_HEIGHT*0.28, bar_root.width, bar_root.height, bar_root.color)
                    new_bar_largest = Bar(bar_root.x, SCREEN_HEIGHT*0.28, bar_largest.width, bar_largest.height, bar_largest.color)
                    del self.bar_list[root_index]
                    self.bar_list.insert(root_index, new_bar_largest)
                    del self.bar_list[largest]
                    self.bar_list.insert(largest, new_bar_root)
                else:
                    arcade.start_render()
                    # "SWAP" BARS
                    bar_root = self.bar_list[root_index]
                    bar_largest = self.bar_list[largest]
                    new_bar_root = Bar(bar_largest.x, SCREEN_HEIGHT*0.28, bar_root.width, bar_root.height, bar_root.color)
                    new_bar_largest = Bar(bar_root.x, SCREEN_HEIGHT*0.28, bar_largest.width, bar_largest.height, bar_largest.color)
                    del self.bar_list[root_index]
                    self.bar_list.insert(root_index, new_bar_largest)
                    del self.bar_list[largest]
                    self.bar_list.insert(largest, new_bar_root)
                    for bar in self.bar_list:
                        bar.draw()
                    time.sleep(0.25)
                    arcade.finish_render()
                # Heapify the new root element to ensure it's the largest
                heapify(areas, heap_size, largest)

        def heapSort(areas):
            n = len(areas)

            # Create a Max Heap from the list
            # The 2nd argument of range means we stop at the element before -1 i.e.
            # the first element of the list.
            # The 3rd argument of range means we iterate backwards, reducing the count
            # of i by 1
            for i in range(n, -1, -1):
                heapify(areas, n, i)

            # Move the root of the max heap to the end of
            for i in range(n - 1, 0, -1):
                areas[i], areas[0] = areas[0], areas[i]
                
                if self.animate == False:
                    # "SWAP" BARS
                    bar_i = self.bar_list[i]
                    bar_0 = self.bar_list[0]
                    new_bar_i = Bar(bar_0.x, SCREEN_HEIGHT*0.28, bar_i.width, bar_i.height, bar_i.color)
                    new_bar_0 = Bar(bar_i.x, SCREEN_HEIGHT*0.28, bar_0.width, bar_0.height, bar_0.color)
                    del self.bar_list[i]
                    self.bar_list.insert(i, new_bar_0)
                    del self.bar_list[0]
                    self.bar_list.insert(0, new_bar_i)
                    heapify(areas, i, 0)
                else:
                    arcade.start_render()
                    # "SWAP" BARS
                    bar_i = self.bar_list[i]
                    bar_0 = self.bar_list[0]
                    new_bar_i = Bar(bar_0.x, SCREEN_HEIGHT*0.28, bar_i.width, bar_i.height, bar_i.color)
                    new_bar_0 = Bar(bar_i.x, SCREEN_HEIGHT*0.28, bar_0.width, bar_0.height, bar_0.color)
                    del self.bar_list[i]
                    self.bar_list.insert(i, new_bar_0)
                    del self.bar_list[0]
                    self.bar_list.insert(0, new_bar_i)
                    for bar in self.bar_list:
                        bar.draw()
                    time.sleep(0.25)
                    arcade.finish_render()
                    heapify(areas, i, 0)

        self.presorted_bars = self.bar_list[:]
        areas = [bar.area for bar in self.bar_list]
        bar_dict = {bar.area:bar for bar in self.bar_list}
        start_time = time.time()
        heapSort(areas)
        self.sort_time = time.time() - start_time
        print("HeapSort time: {} seconds".format(str(self.sort_time)))

    def InsertionSort(self):
        global game
        
        def insertionSort(areas):
            import copy
            for i in range(1, len(areas)):
                item_to_insert = areas[i]
                
                j = i - 1

                if self.animate == True:
                    while j >= 0 and areas[j] > item_to_insert:
                        areas[j + 1] = areas[j]

                        arcade.start_render()
                        # "SWAP" BARS
                        bar_j = self.bar_list[j]
                        bar_j1 = self.bar_list[j+1]
                        new_bar_j = Bar(bar_j1.x, SCREEN_HEIGHT*0.28, bar_j.width, bar_j.height, bar_j.color)
                        new_bar_j1 = Bar(bar_j.x, SCREEN_HEIGHT*0.28, bar_j1.width, bar_j1.height, bar_j1.color)
                        del self.bar_list[j]
                        self.bar_list.insert(j, new_bar_j1)
                        del self.bar_list[j+1]
                        self.bar_list.insert(j+1, new_bar_j)
                        for bar in self.bar_list:
                            bar.draw()
                        time.sleep(0.1)

                        j -= 1
                    # Insert the item
                    areas[j + 1] = item_to_insert

                    # "SWAP" BARS
                    bar_iti = bar_dict[item_to_insert]
                    bar_j1 = self.bar_list[j+1]
                    new_bar_iti = Bar(bar_j1.x, SCREEN_HEIGHT*0.28, bar_iti.width, bar_iti.height, bar_iti.color)
                    del self.bar_list[j+1]
                    self.bar_list.insert(j+1, new_bar_iti)
                    for bar in self.bar_list:
                        bar.draw()
                    time.sleep(0.1)
                    arcade.finish_render()
                else:
                    while j >= 0 and areas[j] > item_to_insert:
                        areas[j + 1] = areas[j]

                        # "SWAP" BARS
                        bar_j = self.bar_list[j]
                        bar_j1 = self.bar_list[j+1]
                        new_bar_j = Bar(bar_j1.x, SCREEN_HEIGHT*0.28, bar_j.width, bar_j.height, bar_j.color)
                        new_bar_j1 = Bar(bar_j.x, SCREEN_HEIGHT*0.28, bar_j1.width, bar_j1.height, bar_j1.color)
                        del self.bar_list[j]
                        self.bar_list.insert(j, new_bar_j1)
                        del self.bar_list[j+1]
                        self.bar_list.insert(j+1, new_bar_j)
                        j -= 1

                    # Insert the item
                    areas[j + 1] = item_to_insert

                    # "SWAP" BARS
                    bar_iti = bar_dict[item_to_insert]
                    bar_j1 = self.bar_list[j+1]
                    new_bar_iti = Bar(bar_j1.x, SCREEN_HEIGHT*0.28, bar_iti.width, bar_iti.height, bar_iti.color)
                    del self.bar_list[j+1]
                    self.bar_list.insert(j+1, new_bar_iti)

        self.presorted_bars = self.bar_list[:]
        areas = [bar.area for bar in self.bar_list]
        bar_dict = {bar.area:bar for bar in self.bar_list}
        start_time = time.time()
        insertionSort(areas)
        self.sort_time = time.time() - start_time
        print("InsertionSort time: {} seconds".format(str(self.sort_time)))

    def SelectionSort(self):
        global game
        
        def selectionSort(areas):
            for i in range(len(areas)):
                lowest_value_index = i
                for j in range(i + 1, len(areas)):
                    if areas[j] < areas[lowest_value_index]:
                        lowest_value_index = j

                areas[i], areas[lowest_value_index] = areas[lowest_value_index], areas[i]

                if self.animate == True:
                    arcade.start_render()
                    # "SWAP" BARS
                    bar_i = self.bar_list[i]
                    bar_lowest = self.bar_list[lowest_value_index]
                    new_bar_i = Bar(bar_lowest.x, SCREEN_HEIGHT*0.28, bar_i.width, bar_i.height, bar_i.color)
                    new_bar_lowest = Bar(bar_i.x, SCREEN_HEIGHT*0.28, bar_lowest.width, bar_lowest.height, bar_lowest.color)
                    del self.bar_list[i]
                    self.bar_list.insert(i, new_bar_lowest)
                    del self.bar_list[lowest_value_index]
                    self.bar_list.insert(lowest_value_index, new_bar_i)
                    for bar in self.bar_list:
                        bar.draw()
                    time.sleep(0.5)
                    arcade.finish_render()
                else:
                    # "SWAP" BARS
                    bar_i = self.bar_list[i]
                    bar_lowest = self.bar_list[lowest_value_index]
                    new_bar_i = Bar(bar_lowest.x, SCREEN_HEIGHT*0.28, bar_i.width, bar_i.height, bar_i.color)
                    new_bar_lowest = Bar(bar_i.x, SCREEN_HEIGHT*0.28, bar_lowest.width, bar_lowest.height, bar_lowest.color)
                    del self.bar_list[i]
                    self.bar_list.insert(i, new_bar_lowest)
                    del self.bar_list[lowest_value_index]
                    self.bar_list.insert(lowest_value_index, new_bar_i)
                    
        self.presorted_bars = self.bar_list[:]
        areas = [bar.area for bar in self.bar_list]
        bar_dict = {bar.area:bar for bar in self.bar_list}
        start_time = time.time()
        selectionSort(areas)
        self.sort_time = time.time() - start_time
        print("SelectionSort time: {} seconds".format(str(self.sort_time)))

class Bar(Shape):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.shape = arcade.create_rectangle_filled(self.x, self.y, self.width, self.height, self.color)
        self.shape_list = arcade.ShapeElementList()
        self.shape_list.append(self.shape)

def main():
    global game
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()