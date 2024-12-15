from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = (
    [
        # Login & Signup using OTP
        path("register/get_otp/", views.getOTP.as_view(), name="get_otp"),
        path("register/verify/", views.VerifyOTP.as_view(), name="verify_otp"),
        path("register/supplier/verify-otp/", views.VerifyOTPForSupplier.as_view(), name="verify_otp_supplier"),
        path("register/bda/verify-otp/", views.VerifyOTPForBDA.as_view(), name="verify_otp_bda"),
        
        # # login & signup using mobileno and password
        # path("register/", views.register, name="register"),
        # path("login/", views.login, name="login"),
        # path("verify/", views.verify_otp, name="verify_otp_page"),
        # path("logout/", views.logout, name="logout"),
        
        # # Update user information
        # path(
        #     "update/<int:pk>",
        #     views.CustomerRetrieveUpdateView.as_view(),
        #     name="customer-retrieve-update",
        # ),
        
        # # reset password using email
        # path(
        #     "reset_password/",
        #     auth_views.PasswordResetView.as_view(
        #         template_name="user/password/forgot-password.html",
        #         email_template_name="user/password/password-reset-email.html",
        #     ),
        #     name="reset_password",
        # ),
        # path(
        #     "reset_password_sent/",
        #     auth_views.PasswordResetDoneView.as_view(
        #         template_name="user/password/password-reset-sent.html"
        #     ),
        #     name="password_reset_done",
        # ),
        # path(
        #     "reset/<uidb64>/<token>",
        #     auth_views.PasswordResetConfirmView.as_view(
        #         template_name="user/password/reset-password-form.html"
        #     ),
        #     name="password_reset_confirm_custom",
        # ),
        # path(
        #     "reset_password_complete/",
        #     auth_views.PasswordResetCompleteView.as_view(
        #         template_name="user/password/password-reset-done.html"
        #     ),
        #     name="password_reset_complete",
        # ),
        # path(
        #     "update/user/profile/",
        #     views.UpdateProfileView.as_view(),
        #     name="auth_update_profile",
        # ),
        # path(
        #     "userprofile/",
        #     views.UserProfileView.as_view(),
        #     name="user_profile",
        # ),
        # path("profilepage/", views.profileUser, name="userprofilepage"),
        # # User order, order-detail, profile,address, coupon, refund
        # path(
        #     "user/ordershistory/",
        #     views.userOrderDetail,
        #     name="orderhistoryuser",
        # ),
        # path(
        #     "user/ordershistory/order-detail/<hashid:pk>/",
        #     views.userOrderDetailExpanded,
        #     name="orderhistorydetail",
        # ),
        # path(
        #     "profile/dashboard/",
        #     views.profileDashboard,
        #     name="profile-dashboard",
        # ),
        # path("profile/address/", views.user_address, name="profile-address"),
        # path(
        #     "profile/address/delete/<hashid:pk>",
        #     views.delete_user_address,
        #     name="delete-profile-address",
        # ),
        # path(
        #     "profile/address/set-primary/<hashid:pk>",
        #     views.set_primary_address,
        #     name="set-primary-profile-address",
        # ),
        # path("profile/payment/", views.user_payment, name="profile-payments"),
        # path("profile/orders/", views.user_orders, name="profile-orders"),
        # path(
        #     "profile/notification/",
        #     views.user_notification,
        #     name="profile-notification",
        # ),
        # path("profile/coupon/", views.user_coupon, name="profile-coupon"),
        # path(
        #     "profile/refund/<hashid:pk>",
        #     views.refund_page,
        #     name="refund-status",
        # ),
        path(
            "user-exists/", views.UserExistView.as_view(), name="user-exists"
        ),
        path("address/", views.UserAddressAPI.as_view(), name="user-address"),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
