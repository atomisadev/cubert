import numpy as np

class Cube:
    def __init__(self):
        self.Wx = np.array([['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']])
        self.Rx = np.array([['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']])
        self.Bx = np.array([['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']])
        self.Ox = np.array([['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']])
        self.Gx = np.array([['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']])
        self.Yx = np.array([['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']])
        self.CV = [0, 0, -1]
        self.front_face_vector = [0, 0, -1]

    def show_cube(self):
        print(f"Front face: {self.front_face_vector}")
        print(15 * "_")
        print("White Face:\n", self.Wx)
        print("Red Face:\n", self.Rx)
        print("Blue Face:\n", self.Bx)
        print("Orange Face:\n", self.Ox)
        print("Green Face:\n", self.Gx)
        print("Yellow Face:\n", self.Yx)

    def get_face_config(self, vector):
        if vector == [0, 1, 0]: return self.Wx
        elif vector == [0, 0, -1]: return self.Gx
        elif vector == [-1, 0, 0]: return self.Ox
        elif vector == [0, 0, 1]: return self.Bx
        elif vector == [1, 0, 0]: return self.Rx
        elif vector == [0, -1, 0]: return self.Yx

    def conf_replacement(self, vector, new_conf):
        if vector == [0, 1, 0]: self.Wx = new_conf
        elif vector == [0, 0, -1]: self.Gx = new_conf
        elif vector == [-1, 0, 0]: self.Ox = new_conf
        elif vector == [0, 0, 1]: self.Bx = new_conf
        elif vector == [1, 0, 0]: self.Rx = new_conf
        elif vector == [0, -1, 0]: self.Yx = new_conf

    def _face_rotation(self, current, rot, axis):
        if rot == 90: sin, cos = 1, 0
        elif rot == -90: sin, cos = -1, 0
        elif rot == 180: sin, cos = 0, -1
        else: return current

        x, y, z = current
        if axis == "X": return [x, (y * cos) - (z * sin), (y * sin) + (z * cos)]
        elif axis == "Y": return [(x * cos) + (z * sin), y, (-x * sin) + (z * cos)]
        elif axis == "Z": return [(x * cos) - (y * sin), (x * sin) + (y * cos), z]
    
    def _YRot(self, vector):
        count = 0
        while True:
            if vector == self.CV:
                return count
            else:
                vector = self._face_rotation(vector, 90, "Y")
                count += 1

    def _move(self, move_type, vector):
        if self.CV == 0:
            self.CV = vector

        if vector[1] == 0:
            if vector[0] != 0: axis = "Z"
            elif vector[0] == 0: axis = "X"
            if vector[0] == -1 or vector[2] == 1: mult = -1
            else: mult = 1
            
            upFace = self._face_rotation(vector, 90 * mult, axis)
            rightFace = self._face_rotation(vector, -90, "Y")
            downFace = self._face_rotation(vector, -90 * mult, axis)
            leftFace = self._face_rotation(vector, 90, "Y")
            backFace = self._face_rotation(vector, 180, "Y")

            vectorConf = self.get_face_config(vector)
            upConf = self.get_face_config(upFace)
            rightConf = self.get_face_config(rightFace)
            downConf = self.get_face_config(downFace)
            leftConf = self.get_face_config(leftFace)
            backConf = self.get_face_config(backFace)

            if move_type == 'side':
                newUp = np.rot90(upConf, k=-1 * (self._YRot(vector)))
                newDown = np.rot90(downConf, k=1 * (self._YRot(vector)))

                lftmov = (leftConf[0][2], leftConf[1][2], leftConf[2][2])
                upmov = (newUp[2][0], newUp[2][1], newUp[2][2])
                rghtmov = (rightConf[0][0], rightConf[1][0], rightConf[2][0])
                dwnmov = (newDown[0][0], newDown[0][1], newDown[0][2])

                newConfLeft = [[leftConf[0][0], leftConf[0][1], dwnmov[0]], [leftConf[1][0], leftConf[1][1], dwnmov[1]], [leftConf[2][0], leftConf[2][1], dwnmov[2]]]
                newConfUp = [[newUp[0][0], newUp[0][1], newUp[0][2]], [newUp[1][0], newUp[1][1], newUp[1][2]], [lftmov[2], lftmov[1], lftmov[0]]]
                newConfRight = [[upmov[0], rightConf[0][1], rightConf[0][2]], [upmov[1], rightConf[1][1], rightConf[1][2]], [upmov[2], rightConf[2][1], rightConf[2][2]]]
                newConfDown = [[rghtmov[2], rghtmov[1], rghtmov[0]], [newDown[1][0], newDown[1][1], newDown[1][2]], [newDown[2][0], newDown[2][1], newDown[2][2]]]
                newConfvector = np.rot90(vectorConf, k=-1)
                
                self.conf_replacement(upFace, newConfUp)
                self.conf_replacement(leftFace, newConfLeft)
                self.conf_replacement(rightFace, newConfRight)
                self.conf_replacement(downFace, newConfDown)
                self.conf_replacement(vector, newConfvector)

            elif move_type == 'upper':
                newUp = np.rot90(upConf, k=-1 * (self._YRot(vector)))
                
                frntmov = (vectorConf[0][0], vectorConf[0][1], vectorConf[0][2])
                rghtmov = (rightConf[0][0],rightConf[0][1],rightConf[0][2])
                backmov = (backConf[0][0],backConf[0][1],backConf[0][2])
                lftmov = (leftConf[0][0],leftConf[0][1],leftConf[0][2])
                
                newConfUp = np.rot9ot(newUp, k=-1)
                newConfLeft = np.array((frntmov, leftConf[1], leftConf[2]))
                newConfBack = np.array((lftmov, backConf[1], backConf[2]))
                newConfRight = np.array((backmov, rightConf[1], rightConf[2]))
                newConfFront = np.array((rghtmov, vectorConf[1], vectorConf[2]))

                self.conf_replacement(upFace, newConfUp)
                self.conf_replacement(leftFace, newConfLeft)
                self.conf_replacement(rightFace, newConfRight)
                self.conf_replacement(vector, newConfFront)
                self.conf_replacement(backFace, newConfBack)

            elif move_type == 'down':
                newDown = np.rot90(downConf, k=1 * (self._YRot(vector)))
                
                newConfDown = np.rot90(newDown, k=-1)
                
                frntmov = (vectorConf[2][0],vectorConf[2][1],vectorConf[2][2])
                lftmov = (leftConf[2][0], leftConf[2][1], leftConf[2][2])
                backmov = (backConf[2][0],backConf[2][1],backConf[2][2])
                rghtmov = (rightConf[2][0],rightConf[2][1],rightConf[2][2] )
                
                newConfRight = np.array((rightConf[0], rightConf[1], frntmov))
                newConfBack = np.array((backConf[0], backConf[1], rghtmov))
                newConfLeft = np.array((leftConf[0], leftConf[1], backmov))
                newConfFront = np.array((vectorConf[0], vectorConf[1], lftmov))

                self.conf_replacement(leftFace, newConfLeft)
                self.conf_replacement(rightFace, newConfRight)
                self.conf_replacement(downFace, newConfDown)
                self.conf_replacement(vector, newConfFront)
                self.conf_replacement(backFace, newConfBack)

        self.CV = vector

    def F(self, times=1):
        for _ in range(times): self._move('side', self.front_face_vector)
    def F_(self, times=1): self.F(times=3)
    
    def R(self, times=1):
        for _ in range(times): self._move('side', self._face_rotation(self.front_face_vector, -90, "Y"))
    def R_(self, times=1): self.R(times=3)
    
    def L(self, times=1):
        for _ in range(times): self._move('side', self._face_rotation(self.front_face_vector, 90, "Y"))
    def L_(self, times=1): self.L(times=3)
    
    def U(self, times=1):
        for _ in range(times): self._move('upper', self.front_face_vector)
    def U_(self, times=1): self.U(times=3)
    
    def B(self, times=1):
        for _ in range(times): self._move('side', self._face_rotation(self.front_face_vector, 180, "Y"))
    def B_(self, times=1): self.B(times=3)
    
    def D(self, times=1):
        for _ in range(times): self._move('down', self.front_face_vector)
    def D_(self, times=1): self.D(times=3)
