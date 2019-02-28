from api.serializers import *
from accounts.models import User,Captain
u=User.objects.get(id=2)
data={ "username":"mahmouddddddzeyada" , 'password':115512, 'confirm_password':115512,
'is_captain':False, 'is_client':True, "governate":"rffr", "city":"rfrf", "phone_number":555,
}
user=User.objects.get(id=2)
ser=UserSerializer(data={
	"email": "dhe@yahoo.com",
	"username": "yowwwussef",

	'is_captain': False,
	'is_client': True,
	"governate": "rffr",
	"city": "rfrf",
	"phone_number": 555,
	"captain": {
		"national_id": 2222555,
		"feedback": "ddccddcc"
	},
})

ser.is_valid()

