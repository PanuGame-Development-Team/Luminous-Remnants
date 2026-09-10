# Luminous-Remnants
### 功能
这是一个由光遇中的星图启发，使用python实现的一个成长纪念册软件。
### 代码构建环境
* Linux Mint 22.2 x64 6.8.0-85-generic
* Python 3.12.3
* pygame 2.5.2 (SDL 2.30.0, Python 3.12.3)
### 使用方法
1. 打包
在 `星座` 文件夹的星座名文件夹内添加 `1.jpg`、`2.jpg`……`n.jpg`，数量参见 `vanillapack` 下 `星数.txt`。

同一文件夹内，添加 `label.txt`，标签这个星座。

所有图片和标签添加完成后，可以回到根目录运行 `mv tools/* .&&python3 packimg.py` 进行打包。
2. 启动星图
在终端运行 `python3 main.py` 即可，每次启动只需要 `main.lrg`、`logo.dat` 两个资源文件，并且确保代码文件不受破坏。使用ESC键退出星图。
3. 备份星图
备份星图只需要备份 `main.lrg`。
### 注意事项
尽管提交 `73a817f` 之前并没有添加 `LICENSE` 文件，但是作者再此声明，从前的提交也按照现在的协议处理。

`customize_settings.py` 中可设置的范围极其广阔，有些极端数值可能导致 `AUTOPLAY` 等精细功能失效，请仅在原设置基础上微调。

### TODO List
1. graph_editor 星图编辑器（定制自己的星图）
2. PySide Renderer Qt渲染器，与pygame并行开发。
3. Lumin Mod System 添加插件系统，在渲染，移动等多出注入钩子，采用eventbus，并且允许覆写多个接口
4. CuteWebLumin 创建并行项目，添加占位WebSocket Renderer，前端使用Emscripten Qt。迁移到手机端。（仅允许AUTOPLAY）
#### finished
1. customize_settings 星图设置