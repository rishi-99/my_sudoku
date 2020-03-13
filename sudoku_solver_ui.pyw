################################################################
############ Developed by - Rishikesh Sarode ###################
################################################################
# rishisarode99@gmail.com


import numpy as np
from tkinter import *
from tkinter import Tk
from tkinter import messagebox,filedialog
import random
from random import shuffle
import threading


class BuilD_UI():

	def __init__(self):
		self.root = Tk()
		self.root.title('My Sudoku Solver')
		self.root.geometry('368x500')
		self.root.resizable(0,0)
		self.solution_no = 0
		self.solution_status = StringVar()
		self.solution_status.set('Py_Sudoku')
	def Display_start(self):


		self.Add_grid()


		def spawn_thread():
			threading.Thread(target=self.Solve).start()
				
		self.Button_(self.root,'Solve',spawn_thread, 20,80,280,50)
		self.next_ = self.Button_(self.root,'>',lambda :self.display_solutions(1),20,40,260,460)
		self.prev_ = self.Button_(self.root,'<',lambda :self.display_solutions(-1),20,40,80,460)
		self.next_['state']='disable'
		self.prev_['state']='disable'
		self.Button_(self.root, 'Clear', self.clear_grid, 20, 90, 190, 50)
		self.Button_(self.root, 'Load sudoku',
					 lambda: self.load_grid(Sudoku(np.zeros((9, 9))).generate_sample(level=self.level.get())), 20, 100,
					 10, 50)


		levels = [1,2,3,4,5,6,7,8,9,10]  # etc
		self.level = IntVar(self.root)
		self.level.set(5)  # default value
		level = OptionMenu(self.root, self.level, *levels)
		level.place(x=290,y=0)

		self.status_label = Label(self.root, textvariable=self.solution_status)
		self.status_label.place(x=150, y=460)
		label = Label(self.root,text= 'Level')
		label.place(x=250, y=3)


		self.Button_(self.root,'About',self.info_display,20,80,0,0)
		self.root.mainloop()

	def info_display(self):

		root = Tk()
		root.title('About')
		root.geometry('400x200')
		TextBox = Text(root, relief=SUNKEN, bd=1, height='12', width='54', wrap=WORD, bg='grey91')
		TextBox.insert(END, "Name          : My_Sudoku\n")
		TextBox.insert(END, "Version       : v_00.1\n")
		TextBox.insert(END, "Uploaded on   : 23/Feb/2020\n")
		TextBox.insert(END, "Developer     : Rishikesh Sarode\n")
		TextBox.insert(END, "Contact       : rishisarode99@gmail.com\n")
		TextBox.insert(END, "Github        : https://github.com/rishi-99\n")
		TextBox.place(x=5, y=5)
		TextBox.config(state=DISABLED)
		root.mainloop()




	def Add_grid(self):

		Layer = Frame(master=self.root,relief=SUNKEN,bd=2,bg='grey91')
		Layer.place(x=4, y=90, height=370, width=360)
		self.grid = []
		x_ = 0
		for x in range(0,360,40):
			rows = []
			y_ = 0
			for y in range(0,360,40):
				s = StringVar()
				color = 'lightgrey'
				if 0<= x_ <=2 or 6<= x_ <=8:
					if 0<= y_ <=2 or 6<= y_ <=8:
						color='darkgrey'
				else:
					if 3<= y_ <=5 :
						color='darkgrey'
				box = Entry(Layer, textvariable=s,bg=color ,relief=SUNKEN,font=("Helvetica", 32), bd=1, width=2,justify='center')
				box.place(x=x,y=y)
				rows.append([box,s,color])
				y_+=1
			self.grid.append(rows)
			x_+=1


	def get_grid_values(self):

		grid_values = []
		Error = False
		for x in self.grid:
			rows = []
			for y in x:
				value = y[1].get()
				try:
					if value != '':
						if 1 <= int(value) <= 9:
							value = int(value)
						else:
							Error = True
							y[0].config({"background": "red"})
					elif value=='':
						value = 0
					else:
						Error=True
						y[0].config({"background": "red"})
				except:
					Error=True
					y[0].config({"background": "red"})
				rows.append(value)
			grid_values.append(rows)
		if Error:
			messagebox.showerror('Bad Values','Values should be between 1-9 !!')

		return np.array(grid_values)



	def load_grid(self,grid):
		self.clear_highlights()
		for x in range(9):
			for y in range(9):
				if grid[x][y] == 0:
					self.grid[x][y][1].set('')
				else:
					self.grid[x][y][1].set(grid[x][y])


	def clear_grid(self):
		self.clear_highlights()
		self.load_grid(np.zeros((9,9)))


	def highlight(self,matrix):

		for x in range(9):
			for y in range(9):
				if matrix[x][y] != 0:
					if self.grid[x][y][2] == "darkgrey":
						self.grid[x][y][0].config({"background": "darkgreen"})
					else:
						self.grid[x][y][0].config({"background": "lightgreen"})


	def clear_highlights(self):
		for x in self.grid:
			for y in x:
				y[0].config({"background": y[2]})


	def Button_(self, root, text, command, h, w, x, y):
		button = Button(master=root, text=text, command=command, fg='grey91')
		button.place(bordermode=OUTSIDE, height=h, width=w, y=y, x=x)
		return button


	def Solve(self):
		self.status_label.set("Solving..")
		self.clear_highlights()
		self.my_grid = self.get_grid_values()
		try:
			self.solution_status.set('Solving ...')
			if self.my_grid.sum()!=0:
				self.solution_no = 0

				self.possible_solutions = Sudoku(self.my_grid).solve()
				if self.possible_solutions:

					self.next_['state'] = 'normal'
					self.display_solutions(1)

				else:
					self.solution_status.set('Solution 0/0 ')
					messagebox.showerror('Cant Solve','No any solution or Bad matrix')
			else:

				self.solution_status.set('Solution 0/0 ')
				messagebox.showerror('Cant Solve', 'Empty Matrix')
		except Exception as e:

			self.solution_status.set('- - -')
			messagebox.showerror('Bad values', 'Bad values in Grid')
		
			
			
	def display_solutions(self,nav):


		self.next_['state'] = 'normal'
		self.prev_['state'] = 'normal'
		self.solution_no+=nav
		if 1< self.solution_no < len(self.possible_solutions):
			pass
		else:
			if self.solution_no == 1:
				self.prev_['state']='disable'
			if self.solution_no==len(self.possible_solutions):
				self.next_['state'] = 'disable'


		self.load_grid(self.possible_solutions[self.solution_no - 1])
		self.solution_status.set('Solution {}/{} '.format(self.solution_no, len(self.possible_solutions)))

		highlights = self.possible_solutions[0] - self.my_grid
		self.highlight(highlights)









class Sudoku():
	
	def __init__(self,grid):
		self.grid=grid
		self.grid_shape = len(grid)
		self.solutions_no = 0

	def perfect_fit(self,x,y,value):
		if value in self.grid[x]:return False
		if value in [self.grid[y_][y] for y_ in range(self.grid_shape)]:return False
		for x_ in range(3):
			for y_ in range(3):
				if self.grid[(x//3)*3+x_][(y//3)*3+y_]==value:return False
		return True

	def get_solutions(self):

		for x in range(self.grid_shape):
			for y in range(self.grid_shape):
				if self.grid[x][y]==0:
					for value in range(1,self.grid_shape+1):
							if self.perfect_fit(x,y,value):
								self.grid[x][y] = value
								self.get_solutions()
								self.grid[x][y] = 0

					return None
		self.solutions.append(self.grid.copy())
		self.solutions_no+=1


	def solve(self):
		self.solutions = []
		self.get_solutions()
		return self.solutions

	def generate_sample(self,level):
			sample = np.zeros((9,9),dtype='int')
			sample[0] =  random.sample([1,2,3,4,5,6,7,8,9],9)
			self.grid =sample
			try:
				self.generate()
			except:
				sample = self.grid

			level_  =int((81*level)/10)
			for x in range(level_):
				sample[random.randint(0,8)][random.randint(0,8)] = 0
			return sample

	def generate(self):
			for x in range(9):
				for y in range(9):
					if self.grid[x][y] == 0:
						for value in range(1, self.grid_shape + 1):
							if self.perfect_fit(x, y, value):
								self.grid[x][y] = value
								self.generate()
								self.grid[x][y] = 0
						return None
			int('x') # force fully exiting the recursion


if __name__ =="__main__":

	a = BuilD_UI()
	a.Display_start()
