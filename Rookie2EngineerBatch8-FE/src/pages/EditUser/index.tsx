import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import PageLayout from "@/components/layouts/PageLayout";
import DateInput from "@/components/UI/Input/DateInput";
import { userService } from "@/api/userService";
import { UserBase, UserUpdate } from "@/types/user";
import { Gender, SortDirection, Type, UserSortOption } from "@/types/enums";
import toast from "@/components/UI/Toast";
import { useNavigate, useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  isNotWeekend,
  isEarlierThanDob,
  isOldEnough,
  dobGreaterThan18,
} from "@utils/DateValidator";
import { useBreadcrumbs } from "@/hooks/useBreadcrumbs";
import { useUserListQueryStore } from "@/stores/userListQueryStore";

export default function EditUser() {
  useBreadcrumbs([
    { label: "Manage User", path: "/manage-user" },
    { label: "Edit User", path: "" },
  ]);
  const {setSortBy, setSortDirection } = useUserListQueryStore()
  const params = useParams();
  const navigate = useNavigate();
  const [originalValues, setOriginalValues] = useState<UserBase>();
  const [formChanged, setFormChanged] = useState(false);
  const [joinDateError, setJoinDateError] = useState("");
  const [dobError, setDobError] = useState("");

  const { register, handleSubmit, setValue, watch, reset } = useForm<UserBase>({
    defaultValues: {
      id: 0,
      first_name: "",
      last_name: "",
      gender: Gender.BLANK,
      date_of_birth: "",
      join_date: "",
      type: Type.STAFF,
    },
  });

  // Use React Query to fetch user data
  const { isLoading } = useQuery({
    queryKey: ["user", params.id],
    queryFn: async () => {
      try {
        const response = await userService.get_user(Number(params.id));

        setOriginalValues(response.data);
        setJoinDateError("");
        reset(response.data);
        return response.data;
      } catch (error) {
        console.error("Error fetching user data:", error);
        navigate(`404`);
      }
    },
    enabled: !!params.id,
  });

  const formValues = watch();
  // const isAdminType = formValues.type === Type.ADMIN;

  useEffect(() => {
    // Guard clause for loading state
    if (!originalValues || isLoading) return;

    // Reset form changed state if date fields are empty
    if (!formValues.date_of_birth || !formValues.join_date) {
      setFormChanged(false);
      return;
    }

    // Check if any relevant fields have been modified
    const hasFieldChanges =
      formValues.gender !== originalValues.gender ||
      formValues.date_of_birth !== originalValues.date_of_birth ||
      formValues.join_date !== originalValues.join_date ||
      formValues.type !== originalValues.type;

    setFormChanged(hasFieldChanges);
  }, [formValues, originalValues, isLoading]);

  const onSubmit = async (data: UserBase) => {
    setJoinDateError("");

    if (!isNotWeekend(data.join_date)) {
      toast({
        content: "Join date cannot be on a Saturday or Sunday",
        alertType: "alert-error",
        duration: 3,
      });
      setValue("join_date", formValues.join_date);
      setJoinDateError(
        "Joined date is Saturday or Sunday. Please select a different date"
      );
      return;
    }

    if (!dobGreaterThan18(data.date_of_birth)) {
      toast({
        content: "User must be at least 18 years old",
        alertType: "alert-error",
        duration: 3,
      });
      setValue("date_of_birth", formValues.date_of_birth);
      setDobError("User is under 18. Please select a different date");
      return;
    }

    if (isEarlierThanDob(data.join_date, data.date_of_birth)) {
      toast({
        content: "Join date cannot be earlier than date of birth",
        alertType: "alert-error",
        duration: 3,
      });
      setValue("join_date", formValues.join_date);
      setJoinDateError(
        "Joined date is not later than Date of Birth. Please select a different date"
      );
      return;
    }

    if (!isOldEnough(data.join_date, data.date_of_birth)) {
      toast({
        content: "User must be at least 18 years old at the time of joining",
        alertType: "alert-error",
        duration: 3,
      });
      setValue("join_date", formValues.join_date);
      setJoinDateError(
        "User is under 18 at the time of joining. Please select a different date"
      );
      return;
    }

    try {
      const updatedUser: UserUpdate = {
        gender: data.gender,
        date_of_birth: new Date(data.date_of_birth).toISOString(),
        join_date: new Date(data.join_date).toISOString(),
        type: data.type,
        location: data.location,
      };

      const response = await userService.update_user(data.id!, updatedUser);

      if (response.data) {
        toast({
          content: "User updated successfully",
          alertType: "alert-success",
          duration: 3,
        });
        setSortBy(UserSortOption.UPDATED_DATE)
        setSortDirection(SortDirection.DESC)
        navigate("/manage-user");
      }
    } catch (error) {
      console.error("Error updating user:", error);
      toast({
        content: "Failed to update user",
        alertType: "alert-error",
        duration: 3,
      });
    }
  };

  return (
    <PageLayout title="Edit User">
      <form onSubmit={handleSubmit(onSubmit)} className="max-w-md">
        <div className="flex items-center mb-4 w-full">
          <label className="w-1/4">First Name</label>
          <input
            id="first_name"
            type="text"
            value={formValues.first_name}
            className="border border-secondary bg-base-300 rounded p-2 h-10 flex-1 cursor-default w-3/4"
            readOnly
          />
        </div>

        <div className="flex items-center mb-4 w-full">
          <label className="w-1/4">Last Name</label>
          <input
            id="last_name"
            type="text"
            value={formValues.last_name}
            className="border border-secondary bg-base-300 rounded p-2 h-10 flex-1 cursor-default w-3/4"
            readOnly
          />
        </div>

        <div className="flex items-center mb-4 w-full">
          <label className="w-1/4">Date of Birth</label>
          <div id="dob" className="flex flex-col w-3/4">
            <DateInput
              id="date_of_birth"
              name="date_of_birth"
              value={formValues.date_of_birth}
              placeholder="dd/mm/yyyy"
              width="w-full"
              className={`${dobError ? "border border-error rounded" : ""}`}
              onChange={(date) => setValue("date_of_birth", date)}
            />
            {dobError && <p className="textarea-xs text-error">{dobError}</p>}
          </div>
        </div>

        <div className="flex items-center mb-4 w-full">
          <label className="w-1/4">Gender</label>
          <div className="flex items-center gap-4">
            <label
              id="female-gender"
              className="flex items-center gap-2 cursor-pointer"
            >
              <input
                type="radio"
                {...register("gender")}
                value={Gender.FEMALE}
                className="radio radio-sm text-primary"
                onClick={() => {
                  if (formValues.gender === Gender.FEMALE)
                    setValue("gender", Gender.BLANK);
                }}
              />
              <span>Female</span>
            </label>
            <label
              id="male-gender"
              className="flex items-center gap-2 cursor-pointer"
            >
              <input
                type="radio"
                {...register("gender")}
                value={Gender.MALE}
                className="radio radio-sm text-primary"
                onClick={() => {
                  if (formValues.gender === Gender.MALE)
                    setValue("gender", Gender.BLANK);
                }}
              />
              <span>Male</span>
            </label>
          </div>
        </div>

        <div className="flex items-center mb-4 w-full">
          <label className="w-1/4">Joined Date</label>
          <div id="joined-date" className="flex flex-col w-3/4">
            <DateInput
              id="joined_date"
              name="join_date"
              value={formValues.join_date}
              width="w-full"
              className={`${
                joinDateError ? "border border-error rounded" : ""
              }`}
              placeholder="dd/mm/yyyy"
              onChange={(date) => setValue("join_date", date)}
            />
            {joinDateError && (
              <p className="textarea-xs text-error">{joinDateError}</p>
            )}
          </div>
        </div>

        <div className="flex items-center mb-4 w-full">
          <label className="w-1/4">Type</label>
          <div className="relative flex-1">
            <select
              id="user_type"
              {...register("type")}
              className="border border-secondary rounded p-2 h-10 w-full"
            >
              {Object.values(Type).map((type) => (
                <option key={type} value={type}>
                  {type.charAt(0).toUpperCase() + type.slice(1).toLowerCase()}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="flex justify-end gap-4">
          <button
            id="save-button"
            type="submit"
            className={`px-6 py-2 rounded btn lg:btn-lg xl:btn-xl text-sm font-normal ${
              formChanged && !isLoading
                ? "bg-primary text-primary-content cursor-pointer"
                : "bg-base-300 text-secondary-500 cursor-not-allowed"
            }`}
            disabled={isLoading || !formChanged}
          >
            Save
          </button>

          <button
            id="cancel-button"
            type="button"
            className="btn lg:btn-lg xl:btn-xl text-sm font-normal"
            onClick={() => navigate("/manage-user")}
          >
            Cancel
          </button>
        </div>
      </form>
    </PageLayout>
  );
}
