from django import forms
from PIL import Image

class GenerateForm(forms.Form):
    #Platform
    platform = forms.ChoiceField(choices=[('windows','Windows'),('linux','Linux (currently unavailable)'),('android','Android'),('macos','macOS')], initial='windows')
    version = forms.ChoiceField(choices=[('master','nightly'),('1.4.0','1.4.0'),('1.3.9','1.3.9'),('1.3.8','1.3.8'),('1.3.7','1.3.7'),('1.3.6','1.3.6'),('1.3.5','1.3.5'),('1.3.4','1.3.4'),('1.3.3','1.3.3')], initial='1.4.0')
    help_text="'master' 是开发版本（夜间构建），具有最新功能，但可能不太稳定"
    delayFix = forms.BooleanField(initial=True, required=False)

    #General
    exename = forms.CharField(label="Name for EXE file", required=True)
    appname = forms.CharField(label="Custom App Name", required=False)
    direction = forms.ChoiceField(widget=forms.RadioSelect, choices=[
        ('incoming', '仅限传入'),
        ('outgoing', '仅限外发'),
        ('both', '双向')
    ], initial='both')
    installation = forms.ChoiceField(label="Disable Installation", choices=[
        ('installationY', '否，启用安装'),
        ('installationN', '是，禁用安装')
    ], initial='installationY')
    settings = forms.ChoiceField(label="Disable Settings", choices=[
        ('settingsY', '否，启用设置'),
        ('settingsN', '是，禁用设置')
    ], initial='settingsY')

    #Custom Server
    serverIP = forms.CharField(label="Host", required=False)
    apiServer = forms.CharField(label="API Server", required=False)
    key = forms.CharField(label="Key", required=False)
    urlLink = forms.CharField(label="Custom URL for links", required=False)
    downloadLink = forms.CharField(label="Custom URL for downloading new versions", required=False)
    compname = forms.CharField(label="Company name",required=False)

    #Visual
    iconfile = forms.FileField(label="通过两者接受会话", required=False, widget=forms.FileInput(attrs={'accept': 'image/png'}))
    logofile = forms.FileField(label="自定义应用程序图标（.png 格式）", required=False, widget=forms.FileInput(attrs={'accept': 'image/png'}))
    iconbase64 = forms.CharField(required=False)
    logobase64 = forms.CharField(required=False)
    theme = forms.ChoiceField(choices=[
        ('light', '白色'),
        ('dark', '深色'),
        ('system', '系统跟随')
    ], initial='system')
    themeDorO = forms.ChoiceField(choices=[('default', '默认'),('override', '覆盖')], initial='default')

    #Security
    passApproveMode = forms.ChoiceField(choices=[('password','通过密码接受会话'),('click','通过点击接受会话'),('password-click','通过两者接受会话')],initial='password-click')
    permanentPassword = forms.CharField(widget=forms.PasswordInput(), required=False)
    runasadmin = forms.ChoiceField(choices=[('false','否'),('true','是')], initial='false')
    denyLan = forms.BooleanField(initial=False, required=False)
    enableDirectIP = forms.BooleanField(initial=False, required=False)
    #ipWhitelist = forms.BooleanField(initial=False, required=False)
    autoClose = forms.BooleanField(initial=False, required=False)

    #Permissions
    permissionsDorO = forms.ChoiceField(choices=[('default', '默认'),('override', '覆盖')], initial='default')
    permissionsType = forms.ChoiceField(choices=[('custom', '自定义'),('full', '完全访问权限'),('view','屏幕共享')], initial='custom')
    enableKeyboard =  forms.BooleanField(initial=True, required=False)
    enableClipboard = forms.BooleanField(initial=True, required=False)
    enableFileTransfer = forms.BooleanField(initial=True, required=False)
    enableAudio = forms.BooleanField(initial=True, required=False)
    enableTCP = forms.BooleanField(initial=True, required=False)
    enableRemoteRestart = forms.BooleanField(initial=True, required=False)
    enableRecording = forms.BooleanField(initial=True, required=False)
    enableBlockingInput = forms.BooleanField(initial=True, required=False)
    enableRemoteModi = forms.BooleanField(initial=False, required=False)

    #Other
    removeWallpaper = forms.BooleanField(initial=True, required=False)

    defaultManual = forms.CharField(widget=forms.Textarea, required=False)
    overrideManual = forms.CharField(widget=forms.Textarea, required=False)

    #custom added features
    cycleMonitor = forms.BooleanField(initial=False, required=False)
    xOffline = forms.BooleanField(initial=False, required=False)
    hidecm = forms.BooleanField(initial=False, required=False)
    removeNewVersionNotif = forms.BooleanField(initial=False, required=False)

    def clean_iconfile(self):
        print("checking icon")
        image = self.cleaned_data['iconfile']
        if image:
            try:
                # Open the image using Pillow
                img = Image.open(image)

                # Check if the image is a PNG (optional, but good practice)
                if img.format != 'PNG':
                    raise forms.ValidationError("仅允许使用 PNG 图像.")

                # Get image dimensions
                width, height = img.size

                # Check for square dimensions
                if width != height:
                    raise forms.ValidationError("自定义应用程序图标尺寸必须是正方形。")
                
                return image
            except OSError:  # Handle cases where the uploaded file is not a valid image
                raise forms.ValidationError("无效的图标文件.")
            except Exception as e: # Catch any other image processing errors
                raise forms.ValidationError(f"错误处理图标: {e}")
