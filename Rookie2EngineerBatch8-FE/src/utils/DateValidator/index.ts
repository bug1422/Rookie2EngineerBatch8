export const dobGreaterThan18 = (dateString: string): boolean => {
    const today = new Date();
    const dob = new Date(dateString);
    
    // Calculate difference in years
    let age = today.getFullYear() - dob.getFullYear();
    
    // Adjust age based on month and day
    const monthDiff = today.getMonth() - dob.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate())) {
        age--;
    }
    
    return age >= 18;
};

export const isNotWeekend = (dateString: string) => {
  const date = new Date(dateString);
  const day = date.getDay();
  // Saturday = 6, Sunday = 0
  if (day == 0 || day == 6) {
    return false;
  }
  return true;
};

export const isEarlierThanDob = (join_date: string, dob: string) => {
  const joinDate = new Date(join_date);
  const dobDate = new Date(dob);
  return joinDate < dobDate;
};

export const isOldEnough = (join_date: string, dob: string) => {
  const joinDate = new Date(join_date);
  const dobDate = new Date(dob);
  let age = joinDate.getFullYear() - dobDate.getFullYear();
  const monthDiff = joinDate.getMonth() - dobDate.getMonth();
  if ((monthDiff < 0) || (monthDiff === 0 && joinDate.getDate() < dobDate.getDate())) {
    age--;
  }
  return age >= 18;
}