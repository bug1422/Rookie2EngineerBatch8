import PageLayout from "@/components/layouts/PageLayout";
import DateInput from "@/components/UI/Input/DateInput";
import { userService } from "@/api/userService";
import { UserBase } from "@/types/user";
import { Gender, Type, Location, UserSortOption, SortDirection } from "@/types/enums";
import toast from "@/components/UI/Toast";
import React, { useState, useEffect } from "react";
import { useForm, Controller } from "react-hook-form";
import { useBreadcrumbs } from "@/hooks/useBreadcrumbs";
import { useNavigate } from "react-router-dom";
import { useAuthStore } from "@/stores/authStore"; // Ensure this path is correct

import { ChevronDown } from "lucide-react";
import { AxiosError } from "axios";
import { useUserListQueryStore } from "@/stores/userListQueryStore";
import { addYears } from "date-fns";
  
const FormField = React.memo(
  ({ label, children }: { label: string; children: React.ReactNode }) => (
    <div className="flex items-start mb-4">
      <label className="w-24 pt-2">{label}</label>
      <div className="flex-1">{children}</div>
    </div>
  )
);

export default function CreateUser() {
  const navigate = useNavigate();
  const { setSortBy, setSortDirection } = useUserListQueryStore();

  // Get the admin location from the auth store
  const admin_Location = useAuthStore.getState().user.location;
  console.log("admin: ", useAuthStore.getState().user.location);

  const INITIAL_STATE: UserBase = {
    id: 0,
    first_name: "",
    last_name: "",
    gender: Gender.BLANK,
    date_of_birth: "",
    join_date: "",
    type: Type.STAFF,
    location: admin_Location as Location, // Use the admin location here
  };

  const {
    register,
    control,
    handleSubmit,
    watch,
    setError,

    setValue,
    formState: { errors, isDirty, isSubmitting, isValid },
  } = useForm<UserBase>({
    defaultValues: INITIAL_STATE,
    mode: "onChange",
  });

  const [adminLocation, setAdminLocation] = useState<Location | null>(null);
  const watchType = watch("type");
  const watchLocation = watch("location");
  const isAdminType = watchType === Type.ADMIN;

  useBreadcrumbs([
    {
      label: "Manage User",
      path: "/manage-user",
    },
    {
      label: "Create New User",
    },
  ]);

  useEffect(() => {
    if (watchType === Type.ADMIN) {
      if (adminLocation === null) {
        setAdminLocation(watchLocation);
      }
    } else if (watchType === Type.STAFF && adminLocation !== null) {
      setValue("location", adminLocation);
    }
  }, [watchType, watchLocation, adminLocation, setValue]);

  const validateForm = (data: UserBase) => {
    const nameRegex = /^[a-zA-Z\s]+$/;
    const firstName = data.first_name.trim();
    const lastName = data.last_name.trim();
    const dob = new Date(data.date_of_birth);
    const joined = new Date(data.join_date);
    const today = new Date();

    const age =
      today.getFullYear() -
      dob.getFullYear() -
      (today < new Date(today.getFullYear(), dob.getMonth(), dob.getDate())
        ? 1
        : 0);

    let hasError = false;

    if (!firstName || !nameRegex.test(firstName) || firstName.length > 128) {
      setError("first_name", {
        message: !firstName
          ? "First name is required."
          : !nameRegex.test(firstName)
          ? "First name cannot contain special characters."
          : "First name must be less than 128 characters.",
      });
      hasError = true;
    }

    if (!lastName || !nameRegex.test(lastName) || lastName.length > 128) {
      setError("last_name", {
        message: !lastName
          ? "Last name is required."
          : !nameRegex.test(lastName)
          ? "Last name cannot contain special characters."
          : "Last name must be less than 128 characters.",
      });
      hasError = true;
    }

    if (!data.date_of_birth || isNaN(dob.getTime()) || age < 18) {
      setError("date_of_birth", {
        message: !data.date_of_birth
          ? "Date of birth is required."
          : isNaN(dob.getTime())
          ? "Invalid date of birth."
          : "User is under 18. Please select a different date",
      });
      hasError = true;
    }

    const dayOfWeek = joined.getDay();
    // Calculate the minimum valid join date (18 years after dob)
    const minJoinDate = addYears(dob, 18);
    if (
      !data.join_date ||
      isNaN(joined.getTime()) ||
      joined < minJoinDate ||
      dayOfWeek === 0 ||
      dayOfWeek === 6
    ) {
      setError("join_date", {
        message: !data.join_date
          ? "Joined date is required."
          : isNaN(joined.getTime())
          ? "Invalid joined date."
          : joined < minJoinDate
          ? "Joined date must be at least 18 years after Date of Birth. Please select a different date"
          : "Joined date is Saturday or Sunday. Please select a different date",
      });
      hasError = true;
    }

    return !hasError;
  };

  const onSubmit = async (data: UserBase) => {
    if (!validateForm(data)) return;

    try {
      const newUser = {
        ...data,
        date_of_birth: new Date(data.date_of_birth).toISOString(),
        join_date: new Date(data.join_date).toISOString(),
      };

      const response = await userService.create_user(newUser);
      if (response.data) {
        toast({
          content: "User created successfully. Redirecting to manage user page",
          alertType: "alert-success",
          duration: 3,
        });
        setSortBy(UserSortOption.UPDATED_DATE);
        setSortDirection(SortDirection.DESC);
        setTimeout(() => {
          navigate("/manage-user");
        }, 3000);
      }
    } catch (error) {
      console.error("Error creating user:", error);
      if (error instanceof AxiosError) {
        if (error.response?.data?.errors) {
          Object.entries(error.response.data.errors).forEach(([key, value]) => {
            setError(key as keyof UserBase, { message: value as string });
          });
        } else {
          toast({
            content: "Failed to create user",
            alertType: "alert-error",
            duration: 3,
          });
        }
      } else {
        toast({
          content: "Failed to create user",
          alertType: "alert-error",
          duration: 3,
        });
      }
    }
  };

  return (
    <PageLayout title="Create New User">
      <form onSubmit={handleSubmit(onSubmit)} className="max-w-md">
        <FormField label="First Name">
          <input
            {...register("first_name", { required: true })}
            className="border border-secondary rounded p-2 h-10 w-full"
          />
          {errors.first_name && (
            <p className="textarea-xs text-error">{errors.first_name.message}</p>
          )}
        </FormField>

        <FormField label="Last Name">
          <input
            {...register("last_name", { required: true })}
            className="border border-secondary rounded p-2 h-10 w-full"
          />
          {errors.last_name && (
            <p className="textarea-xs text-error">{errors.last_name.message}</p>
          )}
        </FormField>

        <FormField label="Date of Birth">
          <Controller
            control={control}
            name="date_of_birth"
            rules={{ required: true }}
            render={({ field }) => (
              <DateInput
                id="dob"
                name="dob"
                placeholder="dd/mm/yyyy"
                value={field.value}
                onChange={field.onChange}
                width="w-88"
              />
            )}
          />
          {errors.date_of_birth && (
            <p className="textarea-xs text-error">
              {errors.date_of_birth.message}
            </p>
          )}
        </FormField>

        <FormField label="Gender">
          <Controller
            control={control}
            name="gender"
            render={({ field }) => (
              <div className="flex items-center gap-4 mt-2">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    className="radio radio-sm text-primary"
                    value={Gender.FEMALE}
                    checked={field.value === Gender.FEMALE}
                    onClick={() => field.value === Gender.FEMALE ? field.onChange(Gender.BLANK) : field.onChange(Gender.FEMALE)}
                    readOnly
                  />
                  <span>Female</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    className="radio radio-sm text-primary"
                    type="radio"
                    value={Gender.MALE}
                    checked={field.value === Gender.MALE}
                    onClick={() => field.value === Gender.MALE ? field.onChange(Gender.BLANK) : field.onChange(Gender.MALE)}
                    readOnly
                  />
                  <span>Male</span>
                </label>
              </div>
            )}
          />
          {errors.gender && (
            <p className="textarea-xs text-error">{errors.gender.message}</p>
          )}
        </FormField>

        <FormField label="Joined Date">
          <Controller
            control={control}
            name="join_date"
            rules={{ required: true }}
            render={({ field }) => (
              <DateInput
                id="joined-date"
                name="joined-date"
                placeholder="dd/mm/yyyy"
                value={field.value}
                onChange={field.onChange}
                width="w-88"
              />
            )}
          />
          {errors.join_date && (
            <p className="textarea-xs text-error">{errors.join_date.message}</p>
          )}
        </FormField>

        <FormField label="Type">
          <div className="relative flex-1">
            <select
              {...register("type")}
              className="border border-secondary rounded p-2 h-10 w-full appearance-none"
            >
              {Object.values(Type).map((type) => (
                <option key={type} value={type}>
                  {type.charAt(0).toUpperCase() + type.slice(1).toLowerCase()}
                </option>
              ))}
            </select>
            <ChevronDown className="absolute right-2 top-2 text-secondary" />
          </div>
        </FormField>

        <FormField label="Location">
          <div className="relative flex-1">
            <select
              {...register("location")}
              disabled={!isAdminType}
              className={`border border-secondary rounded p-2 h-10 w-full appearance-none ${
                !isAdminType ? "bg-gray-200 cursor-default" : ""
              }`}
            >
              {Object.values(Location).map((loc) => (
                <option key={loc} value={loc}>
                  {loc}
                </option>
              ))}
            </select>
            <ChevronDown className="absolute right-2 top-2 text-secondary" />
          </div>
        </FormField>

        <div className="flex justify-end gap-4 mt-6">
          <button
            type="submit"
            disabled={!isDirty || !isValid || isSubmitting}
            className={`px-6 py-2 rounded ${
              isDirty && isValid && !isSubmitting
                ? "bg-primary text-primary-content cursor-pointer"
                : "bg-base-300 text-secondary-500 cursor-not-allowed"
            }`}
          >
            {isSubmitting ? "Saving..." : "Create"}
          </button>
          <button
            id="cancel-button"
            type="button"
            className="border border-secondary px-4 py-2 rounded hover:bg-base-200 hover:cursor-pointer focus:bg-base-300"
            onClick={() => navigate("/manage-user")}
          >
            Cancel
          </button>
        </div>
      </form>
    </PageLayout>
  );
}
