library(ggplot2)
library(dplyr)

# Example: Generating directory names manually
directories <- c("n_64_k_4_t_1_s_42", "n_64_k_4_t_2_s_42", "n_64_k_4_t_3_s_42", "n_64_k_4_t_4_s_42",
                 "n_64_k_4_t_1_s_43", "n_64_k_4_t_2_s_43", "n_64_k_4_t_3_s_43", "n_64_k_4_t_4_s_43",
                 "n_64_k_4_t_1_s_44", "n_64_k_4_t_2_s_44", "n_64_k_4_t_3_s_44", "n_64_k_4_t_4_s_44",
                 "n_64_k_4_t_1_s_45", "n_64_k_4_t_2_s_45", "n_64_k_4_t_3_s_45", "n_64_k_4_t_4_s_45",
                 "n_64_k_4_t_1_s_46", "n_64_k_4_t_2_s_46", "n_64_k_4_t_3_s_46", "n_64_k_4_t_4_s_46")
file_paths <- paste0("data/exp1/", directories, "/nbh_frequencies.csv")
merged_data <- data.frame()
for (file_path in file_paths) {
    print(file_path)
    if (file.exists(file_path)) {
        dat <- read.csv(file_path)
        merged_data <- rbind(merged_data, dat)
    }
}

merged_data$time_per_run <- as.factor(merged_data$time_per_run)

p <- ggplot(merged_data, aes(x=freq, group=time_per_run, color=time_per_run)) +
     stat_ecdf() +
     coord_cartesian(xlim=c(NA, 200)) +
     theme_bw() +
     xlab("Frequency") +
     ylab("ECDF") +
     theme(legend.position=c(0.8, 0.3), legend.box.background = element_rect(colour = "black"))

ggsave("data/nbh_frequencies_different_t_ecdf.pdf", p, width=5, height=3)
