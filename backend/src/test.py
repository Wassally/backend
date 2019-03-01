from accounts.serializers import *
from accounts.models import User,Captain
u=User.objects.get(id=2)
data={ "username":"mahmouddddddzeyada" , 'password':115512, 'confirm_password':115512,
'is_captain':False, 'is_client':True, "governate":"rffr", "city":"rfrf", "phone_number":555,
}
user=User.objects.get(id=2)
ser=UserSerializer(data={
	"email": "dhe@yahoo.com",
	"username": "test1",
	"password":"555",
	"confirm_password": "555",

	'is_captain': False,
	'is_client': True,
	"governate": "rffr",
	"city": "rfrf",
	"phone_number": 555,
	"captain": {
		"national_id": 1112222555,
		"feedback": "tset"
	},
})

ser.is_valid()

