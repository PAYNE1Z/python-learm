## ���������


### һ����������������ԣ�����ʲô�ô���˵˵�����⡣

### ����������ԺͶ����������ʲô����?
### ����������̱������������̵�������Ӧ�ó���?
### �ġ���Ͷ������ڴ�������α���ġ�
### �塢ʲô�ǰ󶨵�����ķ������󶨵���ķ���������󶨵ĺ�������ζ��壬��ε��ã���˭�ã���ʲô����
### ����ʹ��ʵ������ ��ȡ�����á�ɾ�� ����, �ֱ�ᴥ�����ʲô˽�з���

 class A(object):
     pass

 a = A()

 a["key"] = "val"
 a = a["key"]
 del a["key"]
### �ߡ�python�о��������ʽ�������

### �ˡ�����ʾ��, ��������������ʽ�Ż����´���

   def exc1(host,port,db,charset,sql):
       conn=connect(host,port,db,charset)
       conn.execute(sql)
       return xxx
   def exc2(host,port,db,charset,proc_name)
       conn=connect(host,port,db,charset)
       conn.call_proc(sql)
       return xxx
   # ÿ�ε��ö���Ҫ�ظ�����һ�Ѳ���
   exc1('127.0.0.1',3306,'db1','utf8','select * from tb1;')
   exc2('127.0.0.1',3306,'db1','utf8','�洢���̵�����')

### �š�ʾ��1, �������´��룬 �����ʲô��

  class People(object):
      __name = "luffy"
      __age = 18

  p1 = People()
  print(p1.__name, p1.__age)
### ʮ��ʾ��2, �������´��룬 �����ʲô��

class People(object):

   def __init__(self):
       print("__init__")

   def __new__(cls, *args, **kwargs):
       print("__new__")
       return object.__new__(cls, *args, **kwargs)

People()
### ʮһ����򵥽���Python�� staticmethod����̬�������� classmethod���෽����, ���ֱ𲹳����ִ�����з�����

class A(object):

   def foo(self, x):
       print("executing foo(%s, %s)" % (self,x))

   @classmethod
   def class_foo(cls, x):
       print("executing class_foo(%s, %s)" % (cls,x))

   @staticmethod
   def static_foo(x):
       print("executing static_foo(%s)" % (x))

a = A()
### ʮ������ִ�����´��룬���ʹ���ԭ�򣬲���������

class Dog(object):

   def __init__(self,name):
       self.name = name

   @property
   def eat(self):
       print(" %s is eating" %self.name)

d = Dog("ChenRonghua")
d.eat()
### ʮ����������δ��������������ʲô������͡�

class Parent(object):
   x = 1

class Child1(Parent):
   pass

class Child2(Parent):
   pass

print(Parent.x, Child1.x, Child2.x)
Child1.x = 2
print(Parent.x, Child1.x, Child2.x)
Parent.x = 3
print(Parent.x, Child1.x, Child2.x)

# 1 1 1 �̳��Ը����������x�����Զ�һ����ָ��ͬһ���ڴ��ַ
# 1 2 1 ����Child1��Child1��xָ�����µ��ڴ��ַ
# 3 2 3 ����Parent��Parent��xָ�����µ��ڴ��ַ
### ʮ�ġ����ؼ̳е�ִ��˳������������������ʲô�������͡�

class A(object):
   def __init__(self):
       print('A')
       super(A, self).__init__()

class B(object):
   def __init__(self):
       print('B')
       super(B, self).__init__()

class C(A):
   def __init__(self):
       print('C')
       super(C, self).__init__()

class D(A):
   def __init__(self):
       print('D')
       super(D, self).__init__()

class E(B, C):
   def __init__(self):
       print('E')
       super(E, self).__init__()

class F(C, B, D):
   def __init__(self):
       print('F')
       super(F, self).__init__()

class G(D, B):
   def __init__(self):
       print('G')
       super(G, self).__init__()

if __name__ == '__main__':
   g = G()
   f = F()

# G
# D
# A
# B
#
# F
# C
# B
# D
# A
���дһ�η��϶�̬���ԵĴ���.

�ܶ�ͬѧ����ѧ�������������﷨��ȴ��Ȼд�����������ĳ���ԭ����ʲô�أ�ԭ�������Ϊ�㻹û����һ������������������������ģ���������ʲô������ģ���Լ����ͨ��������������ĳ���http://www.cnblogs.com/alex3714/articles/5188179.html ��blog����������

��дһ��С��Ϸ���˹���վ��2����ɫ���˺͹�����Ϸ��ʼ������2���ˣ�3�����������ս���˱���ҧ�˻��Ѫ�������˴���Ҳ��Ѫ�������˵Ĺ��������߱��Ĺ��ܶ���һ����ע�⣬�밴��14����ģ�ķ�ʽ������ࡣ

��д����, ��Ԫ���п��ư��Զ�������������Զ���ɴ�д.

��д����, ��Ԫ���п����Զ����������init����.

��д����, ��дһ��ѧ����, Ҫ����һ��������������, ͳ���ܹ�ʵ�����˶��ٸ�ѧ��.
��д����, A �̳��� B, �����඼ʵ���� handle ����, �� A �е� handle �����е��� B �� handle ����
��д����, ����������Ҫ��


�Զ����û���Ϣ���ݽṹ�� д���ļ�, Ȼ���ȡ������, ����jsonģ��������ݵ����л��ͷ����л�
e.g
{
    "egon":{"password":"123",'status':False,'timeout':0},
    "alex":{"password":"456",'status':False,'timeout':0},
}
�����û��࣬���巽��db������ ִ��obj.db�����õ��û����ݽṹ
�ڸ�����ʵ�ֵ�¼���˳�����, ��¼�ɹ���״̬(status)�޸�ΪTrue, �˳���״̬�޸�ΪFalse(�˳�Ҫ�ж��Ƿ��ڵ�¼״̬).��������������ν���������ʱ��(�´ε�¼����͵�ǰʱ��Ƚϴ���10�뼴�������¼)