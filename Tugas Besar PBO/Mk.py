from aplikasidb import DBConnection as mydb

class matakuliah:

    def __init__(self):
        self.__id = None
        self.__namamhs = None
        self.__namamk = None
        self.__sks = None
        self.__semester = None
        self.conn = None
        self.affected = None
        self.result = None

    @property
    def id(self):
        return self.__id

    @property
    def namamhs(self):
        return self.__namamhs

    @namamhs.setter
    def namamhs(self, value):
        self.__namamhs = value

    @property
    def namamk(self):
        return self.__namamk

    @namamk.setter
    def namamk(self, value):
        self.__namamk = value

    @property
    def sks(self):
        return self.__sks

    @sks.setter
    def sks(self, value):
        self.__sks = value

    @property
    def semester(self):
        return self.__semester

    @semester.setter
    def semester(self, value):
        self.__semester = value

    def _connect(self):
        self.conn = mydb()

    def _disconnect(self):
        if self.conn:
            self.conn.disconnect()

    def simpan(self):
        self.conn = mydb()
        val = (self.__namamhs, self.__namamk, self.__sks, self.__semester)
        sql="INSERT INTO matakuliah (namamhs, namamk, sks, semester) VALUES " + str(val)
        self.affected = self.conn.insert(sql)
        self.conn.disconnect
        return self.affected

    def getByNAMAMHS(self, namamhs):
        self._connect()
        sql = "SELECT * FROM matakuliah WHERE namamhs=%s"
        self.result = self.conn.findOne(sql, (namamhs,))
        if self.result:
            self.__namamhs, self.__namamk, self.__sks, self.__semester = self.result[1:]
            self.affected = self.conn.cursor.rowcount
        else:
            self.__namamhs = self.__namamk = self.__sks = self.__semester = ''
            self.affected = 0
        self._disconnect()
        return self.result

    def update(self, id):
        self._connect()
        val = (self.__namamk, self.__sks, id)
        sql = "UPDATE matakuliah SET namamk = %s, sks = %s WHERE id = %s"
        self.affected = self.conn.update(sql, val)
        self._disconnect()
        return self.affected

    def updateByNAMAMHS(self, namamhs):
        self._connect()
        val = (self.__namamk, self.__sks, namamhs)
        sql = "UPDATE matakuliah SET namamk = %s, sks = %s WHERE namamhs = %s"
        self.affected = self.conn.update(sql, val)
        self._disconnect()
        return self.affected

    def delete(self, id):
        self._connect()
        sql = "DELETE FROM matakuliah WHERE id = %s"
        self.affected = self.conn.delete(sql, (id,))
        self._disconnect()
        return self.affected

    def deleteByNAMAMHS(self, namamhs):
        self._connect()
        sql = "DELETE FROM matakuliah WHERE namamhs = %s"
        self.affected = self.conn.delete(sql, (namamhs,))
        self._disconnect()
        return self.affected

    def getByID(self, id):
        self._connect()
        sql = "SELECT * FROM matakuliah WHERE id = %s"
        self.result = self.conn.findOne(sql, (id,))
        if self.result:
            self.__namamhs, self.__namamk, self.__sks, self.__semester = self.result[1:]
        self._disconnect()
        return self.result

    def getAllData(self):
        self._connect()
        sql = "SELECT * FROM matakuliah"
        self.result = self.conn.findAll(sql)
        self._disconnect()
        return self.result

# Tampilkan Data
A = matakuliah()
B = A.getAllData()
print(B)
