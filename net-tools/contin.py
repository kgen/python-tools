# coroutine.py
# coding:utf-8
import greenlet

# 用greenlet模拟lua的coroutine.wrap语法
def co_yield(*args, **kwargs):
	return greenlet.getcurrent().parent.switch(*args, **kwargs)

class wrap(object):
	def __init__(self, fn):
		self.gl = greenlet.greenlet(fn)
	
	def __call__(self, *args, **kwargs):
		return self.resume(*args, **kwargs)
	
	def resume(self, *args, **kwargs):
		return self.gl.switch(*args, **kwargs)

	def is_running(self):
		return bool(self.gl)
		
	def is_dead(self):
		return self.gl.dead
		
	def get_parent(self):
		return self.gl.parent


# 示例代码
if __name__ == "__main__":

	def on_engine_async_model_ok_callback(model, co):
		# resume并传参model给yield（本例中这时顺便取得了return value）
		rval = co(model)
		print "rval", rval
			
	def load_model(model_file):
		print "call engine.load_async_model"
		return co_yield()
		
	def do_something_with_async_model_in_sync_codes(model_file, x, y, z):
		pid = 1000
		model = load_model(model_file)
		print "load model ok: ", model
		return pid

	# 得到一个coroutine wrapper
	co = wrap(do_something_with_async_model_in_sync_codes)
	# 传参，启动
	co("goblin.gim", 1, 2, 3)

	# 模拟异步加载需要0.5秒
	import time
	print "sleep 0.5sec..\n"
	time.sleep(0.5)

	# 模拟引擎的异步模型加载完成回调的触发
	on_engine_async_model_ok_callback("<goblin.gim>", co)